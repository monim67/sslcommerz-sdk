import uuid

from .enums import TransactionStatus
from .exceptions import (
    InvalidPaymentException,
    SessionDoesNotExistException,
    TotalAmountTamperedException,
    TranIdReuseException,
)
from .services import PayloadSchema, sslcommerz_exception_context


DEFAULT_OPTIONS = dict(
    product_profile="general",
    product_name="any",
    product_category="any",
    shipping_method="NO",
)


class PaymentHandler:
    def __init__(self, model, orm_adapter, store_provider):
        self.model = model
        self.orm_adapter = orm_adapter
        self.store_provider = store_provider

    def get_or_create_session(self, store, **kwargs):
        options = {**DEFAULT_OPTIONS, **kwargs}
        tran_id = options.get("tran_id")
        with sslcommerz_exception_context(tran_id):
            self.store_provider.validate_store(store)
            if self._get_existing_session(tran_id=tran_id):
                raise TranIdReuseException("Transaction ID already exists in database")
            pending_session = self._get_pending_session(tran_id=tran_id)
            if pending_session:
                if self._session_and_options_conflicts(pending_session, options):
                    raise TotalAmountTamperedException(
                        "Basket modified for ongoing transaction"
                    )
                return pending_session, False
            return self._create_new_session_from_options(store, options), True

    def verify_transaction(self, payload):
        tran_id = payload.get("tran_id", None)
        with sslcommerz_exception_context(tran_id):
            payload = PayloadSchema().load(payload)
            # SSLCOMMERZ does not send sesssionkey with IPN (which does not make any sense),
            # So we will use value_d to identify session until SSLCOMMERZ fixes it.
            session = self.orm_adapter.get_session_instance_by_pk(
                model=self.model, pk=payload["value_d"]
            )
            if session is None:
                raise SessionDoesNotExistException("Session not found")
            if self._session_and_payload_conflicts(session, payload):
                raise InvalidPaymentException("Session payable mismatches with payload")
            if session.status != TransactionStatus.PENDING:
                return session, False
            store = self.store_provider.get_store_by_id(payload["store_id"])
            validation_response = store.validate_ipn_payload(payload=payload)
            self._update_session_from_payload(session, payload, validation_response)
            self.orm_adapter.save_session_instance(
                self.model,
                session,
                payload=payload,
                validation_response=validation_response,
            )
            return session, True

    def _get_existing_session(self, tran_id):
        existing_sessions = self.orm_adapter.get_session_instance_iterator(
            self.model, tran_id, [TransactionStatus.VALID]
        )
        return next(existing_sessions, None)

    def _get_pending_session(self, tran_id):
        pending_sessions = self.orm_adapter.get_session_instance_iterator(
            self.model, tran_id, [TransactionStatus.PENDING]
        )
        return next(pending_sessions, None)

    def _create_new_session_from_options(self, store, options):
        session_pk = str(uuid.uuid4())
        session_props = dict(**options, value_d=session_pk)
        # value_d is used to identify session later while verifying transaction
        response_json = store.create_session(**session_props)
        model_props = session_props.copy()
        for key in ("ipn_url", "success_url", "fail_url", "cancel_url"):
            del model_props[key]
        session = self.orm_adapter.create_session_instance(
            self.model,
            **model_props,
            id=session_pk,
            store_id=store.id,
            sessionkey=response_json["sessionkey"],
            redirect_url=response_json["GatewayPageURL"],
        )
        self.orm_adapter.save_session_instance(self.model, session)
        return session

    def _session_and_options_conflicts(self, session, payload):
        if session.total_amount != payload["total_amount"]:
            return True
        if session.currency != payload["currency"]:
            return True

    def _session_and_payload_conflicts(self, session, payload):
        if session.total_amount != payload["currency_amount"]:
            return True
        if session.currency != payload["currency_type"]:
            return True

    def _update_session_from_payload(self, session, payload, validation_response):
        session.status = payload["status"]
        session.tran_date = payload["tran_date"]
        session.bank_tran_id = payload["bank_tran_id"]
        session.currency_amount = payload["currency_amount"]
        session.currency_rate = payload["currency_rate"]
        session.currency_type = payload["currency_type"]
        session.amount = payload["amount"]
        session.currency = payload["currency"]
        # Optional fields
        session.val_id = payload.get("val_id")
        session.store_amount = payload.get("store_amount")
        session.card_type = payload.get("card_type")
        session.card_no = payload.get("card_no")
        session.card_issuer = payload.get("card_issuer")
        session.card_brand = payload.get("card_brand")
        session.card_issuer_country = payload.get("card_issuer_country")
        session.card_issuer_country_code = payload.get("card_issuer_country_code")
        session.risk_level = payload.get("risk_level")
        session.risk_title = payload.get("risk_title")
        # Payloads
        session.ipn_payload = payload["json"]
        if validation_response:
            session.validation_response = validation_response["json"]
