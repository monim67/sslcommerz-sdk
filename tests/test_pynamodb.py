from django.test import LiveServerTestCase
from moto import mock_dynamodb2

from sslcommerz_sdk.handlers import PaymentHandler
from sslcommerz_sdk.orm_adapters.pynamodb import (
    PynamodbORMAdapter,
    sslcommerz_session_pynamodb_model_factory,
)
from sslcommerz_sdk.store import SslcommerzStore
from sslcommerz_sdk.store_providers import MultpleStoreProvider

from .services import DEFAULT_KWARGS, generate_test_payload

SslcommerzSession = sslcommerz_session_pynamodb_model_factory(region="us-east-1")


class DjangoTests(LiveServerTestCase):
    def setUp(self):
        store_kwargs = dict(
            base_url=self.live_server_url,
            session_url="/session",
            validation_url="/validate",
        )
        self.store = SslcommerzStore(
            store_id="store_id", store_passwd="store_passwd", **store_kwargs
        )
        self.payment_handler = PaymentHandler(
            model=SslcommerzSession,
            orm_adapter=PynamodbORMAdapter(),
            store_provider=MultpleStoreProvider(
                get_store_by_id=lambda store_id: self.store
            ),
        )

    @mock_dynamodb2
    def test_payment(self):
        SslcommerzSession.create_table(wait=True)
        session, created = self.payment_handler.get_or_create_session(
            store=self.store, tran_id="valid_transaction", **DEFAULT_KWARGS,
        )
        self.assertTrue(created)
        test_payload = generate_test_payload(session.id, "store_passwd")
        session, verified_right_now = self.payment_handler.verify_transaction(
            payload=test_payload
        )
        self.assertTrue(verified_right_now)
