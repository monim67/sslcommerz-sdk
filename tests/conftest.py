from typing import Iterator

import pytest
from moto import mock_dynamodb
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from sslcommerz_sdk.contrib.django_app.models import SslcommerzSession
from sslcommerz_sdk.handlers import PaymentHandler
from sslcommerz_sdk.orm_adapters.django import DjangoORMAdapter
from sslcommerz_sdk.orm_adapters.pynamodb import (
    PynamodbORMAdapter,
    sslcommerz_session_pynamodb_model_factory,
)
from sslcommerz_sdk.orm_adapters.sqlalchemy import (
    SqlalchemyORMAdapter,
    sslcommerz_session_sqlalchemy_model_factory,
)
from sslcommerz_sdk.store import SslcommerzStore
from sslcommerz_sdk.store_providers import MultpleStoreProvider


@pytest.fixture
def store() -> SslcommerzStore:
    return SslcommerzStore(store_id="store_id", store_passwd="store_passwd")


@pytest.fixture
def django_payment_handler(store: SslcommerzStore, db) -> Iterator[PaymentHandler]:
    payment_handler = PaymentHandler(
        model=SslcommerzSession,
        orm_adapter=DjangoORMAdapter(),
        store_provider=MultpleStoreProvider(get_store_by_id=lambda store_id: store),
    )
    yield payment_handler


@pytest.fixture
def sqlalchemy_payment_handler(store: SslcommerzStore) -> Iterator[PaymentHandler]:
    engine = create_engine("sqlite:///:memory:")
    db_session = scoped_session(sessionmaker(bind=engine))
    Base = declarative_base()
    SslcommerzSession = sslcommerz_session_sqlalchemy_model_factory(Base)
    Base.metadata.create_all(engine)
    payment_handler = PaymentHandler(
        model=SslcommerzSession,
        orm_adapter=SqlalchemyORMAdapter(db_session=db_session),
        store_provider=MultpleStoreProvider(get_store_by_id=lambda store_id: store),
    )
    yield payment_handler
    Base.metadata.drop_all(engine)


@pytest.fixture
def pynamodb_payment_handler(store: SslcommerzStore) -> Iterator[PaymentHandler]:
    SslcommerzSession = sslcommerz_session_pynamodb_model_factory(region="us-east-1")
    payment_handler = PaymentHandler(
        model=SslcommerzSession,
        orm_adapter=PynamodbORMAdapter(),
        store_provider=MultpleStoreProvider(get_store_by_id=lambda store_id: store),
    )
    with mock_dynamodb():
        SslcommerzSession.create_table(wait=True)
        yield payment_handler


@pytest.fixture(
    params=[
        django_payment_handler,
        sqlalchemy_payment_handler,
        pynamodb_payment_handler,
    ]
)
def payment_handler(request: pytest.FixtureRequest) -> PaymentHandler:
    return request.getfixturevalue(request.param.__name__)
