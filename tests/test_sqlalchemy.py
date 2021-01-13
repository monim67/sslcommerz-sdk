from django.test import LiveServerTestCase
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from sslcommerz_sdk.handlers import PaymentHandler
from sslcommerz_sdk.orm_adapters.sqlalchemy import (
    SqlalchemyORMAdapter,
    sslcommerz_session_sqlalchemy_model_factory,
)
from sslcommerz_sdk.store import SslcommerzStore
from sslcommerz_sdk.store_providers import MultpleStoreProvider

from .services import DEFAULT_KWARGS, generate_test_payload


engine = create_engine("sqlite+pysqlite:///sqlalchemy.sqlite3")
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
SslcommerzSession = sslcommerz_session_sqlalchemy_model_factory(Base)


class DjangoTests(LiveServerTestCase):
    def tearDown(self):
        Base.metadata.drop_all(engine)

    def setUp(self):
        Base.metadata.create_all(engine)
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
            orm_adapter=SqlalchemyORMAdapter(db_session=db_session),
            store_provider=MultpleStoreProvider(
                get_store_by_id=lambda store_id: self.store
            ),
        )

    def test_payment(self):
        session, created = self.payment_handler.get_or_create_session(
            store=self.store, tran_id="valid_transaction", **DEFAULT_KWARGS,
        )
        self.assertTrue(created)
        test_payload = generate_test_payload(session.id, "store_passwd")
        session, verified_right_now = self.payment_handler.verify_transaction(
            payload=test_payload
        )
        self.assertTrue(verified_right_now)
