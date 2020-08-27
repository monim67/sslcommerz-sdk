import uuid
from decimal import Decimal

from .enums import TransactionStatus
from .exceptions import (
    InvalidPaymentException,
    SessionDoesNotExistException,
    TotalAmountTamperedException,
    TranIdReuseException,
)
from .helpers import sslcommerz_exception_context


class PaymentHandler:

    def __init__(self, model, queryset_builder, store):
        self.model = model
        self.store = store
        self.queryset = queryset_builder.from_model(self.model)

    def get_or_create_session(self, **kwargs):
        tran_id = kwargs.get("tran_id")
        with sslcommerz_exception_context(tran_id):
            if self._tran_id_exists(tran_id=tran_id):
                raise TranIdReuseException("Transaction ID already exists in database")
            pending_session = self._get_pending_session(tran_id=tran_id)
            if pending_session:
                if self._session_and_payload_conflicts(pending_session, kwargs):
                    raise TotalAmountTamperedException(
                        "Basket modified for transaction ongoing"
                    )
                return False, pending_session
            return True, self._create_new_session_from_kwargs(**kwargs)

    def verify_transaction(self, payload):
        tran_id = payload.get("tran_id", None)
        with sslcommerz_exception_context(tran_id):
            # SSLCommerz does not send sesssionkey with IPN (which does not make any sense),
            # So we will use value_d to identify session until SSLCommerz fixes it.
            value_d = payload["value_d"]
            if not self.queryset.filter(value_d=value_d).exists():
                raise SessionDoesNotExistException("Session not found")
            session = self.queryset.get(value_d=value_d)
            if self._session_and_payload_conflicts(session, payload):
                raise InvalidPaymentException("Session payable mismatches with payload")
            if session.status != TransactionStatus.PENDING:
                return session, False
            response_json = self.store.validate_ipn_payload(payload)
            session.status = (response_json or payload).get("status")
            self._update_session_from_payload(session, payload)
            self.queryset.save_model_instance(self.model, session)
            return session, True

    def _tran_id_exists(self, tran_id):
        return (
            self.queryset.filter(tran_id=tran_id)
            .filter_in(status=(TransactionStatus.VALID, TransactionStatus.VALIDATED))
            .exists()
        )

    def _get_pending_session(self, tran_id):
        return self.queryset.filter(
            tran_id=tran_id, status=TransactionStatus.PENDING
        ).first()

    def _create_new_session_from_kwargs(self, **kwargs):
        # value_d is used to identify session while verifying transaction
        session_props = dict(**kwargs, value_d=str(uuid.uuid4()))
        response_json = self.store.create_session(**session_props)
        model_props = session_props.copy()
        for key in ("ipn_url", "success_url", "fail_url", "cancel_url"):
            del model_props[key]
        session = self.queryset.create_model_instance(
            self.model,
            **model_props,
            sessionkey=response_json["sessionkey"],
            redirect_url=response_json["GatewayPageURL"],
        )
        self.queryset.save_model_instance(self.model, session)
        return session

    def _session_and_payload_conflicts(self, session, payload):
        if session.total_amount != Decimal(payload.get("currency_amount")):
            return True
        if session.currency != payload.get("currency_type"):
            return True

    def _update_session_from_payload(self, session, payload):
        session.val_id = payload.get("val_id", None)
        session.tran_date = payload["tran_date"]
        session.bank_tran_id = payload["bank_tran_id"]
        session.currency_amount = payload["currency_amount"]
        session.currency_rate = payload["currency_rate"]
        session.currency_type = payload["currency_type"]
        session.amount = payload["amount"]
        session.currency = payload["currency"]
        session.store_amount = payload.get("store_amount", None)
        session.card_type = payload.get("card_type", None)
        session.card_no = payload.get("card_no", None)
        session.card_issuer = payload.get("card_issuer", None)
        session.card_brand = payload.get("card_brand", None)
        session.card_issuer_country = payload.get("card_issuer_country", None)
        session.card_issuer_country_code = payload.get("card_issuer_country_code", None)
        session.risk_level = payload.get("risk_level", None)
        session.risk_title = payload.get("risk_title", None)
