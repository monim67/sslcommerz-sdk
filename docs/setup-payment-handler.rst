##############################
Setup Payment Handler
##############################


.. _setup-django:

********************
Django ORM
********************

Add :code:`"sslcommerz_sdk.contrib.django_app"` to INSTALLED_APPS, and migrate.

.. code-block:: bash

    python manage.py migrate

Get started with following :code:`payment_handler.py` file for Django ORM.
If you need to configure multiple store checkout `Next Steps`_.

.. code-block:: python

    from sslcommerz_sdk.contrib.django_app.models import SslcommerzSession
    from sslcommerz_sdk.handlers import PaymentHandler
    from sslcommerz_sdk.orm_adapters.django import DjangoORMAdapter
    from sslcommerz_sdk.store import SslcommerzStore
    from sslcommerz_sdk.store_providers import SingleStoreProvider

    store = SslcommerzStore(
        store_id="YOUR_STORE_ID",
        store_passwd="YOUR_STORE_PASSWORD",
        base_url="https://sandbox.sslcommerz.com",
    )
    payment_handler = PaymentHandler(
        model=SslcommerzSession,
        orm_adapter=DjangoORMAdapter(),
        store_provider=SingleStoreProvider(store=store),
    )

When you are done, checkout `Next Steps`_.


.. _setup-sqlalchemy:

********************
Sqlalchemy
********************

Get started with following :code:`payment_handler.py` file for Sqlalchemy and Flask-Sqlalchemy.
If you need to configure multiple store checkout `Next Steps`_.

.. code-block:: python

    from sslcommerz_sdk.handlers import PaymentHandler
    from sslcommerz_sdk.orm_adapters.sqlalchemy import (
        SqlalchemyORMAdapter,
        sslcommerz_session_sqlalchemy_model_factory,
    )
    from sslcommerz_sdk.store import SslcommerzStore
    from sslcommerz_sdk.store_providers import SingleStoreProvider

    # TODO: import your declarative base or db.Model as BaseModel
    # TODO: import sqlalchemy session or db.session as db_session

    SslcommerzSession = sslcommerz_session_sqlalchemy_model_factory(BaseModel)
    store = SslcommerzStore(
        store_id="YOUR_STORE_ID",
        store_passwd="YOUR_STORE_PASSWORD",
        base_url="https://sandbox.sslcommerz.com",
    )
    payment_handler = PaymentHandler(
        model=SslcommerzSession,
        orm_adapter=SqlalchemyORMAdapter(db_session=db_session),
        store_provider=SingleStoreProvider(store=store),
    )

Then you can create the model generating alembic migration files or
directly from a python shell prompt.

.. code-block:: python

    # Run in python shell
    from app.db import engine
    from .payment_handler import SslcommerzSession
    SslcommerzSession.__table__.create(engine)

When you are done, checkout `Next Steps`_.


.. _setup-pynamodb:

********************
PynamoDB
********************

Get started with following :code:`payment_handler.py` file for PynamoDB.
If you need to configure multiple store checkout `Next Steps`_.

.. code-block:: python

    from sslcommerz_sdk.handlers import PaymentHandler
    from sslcommerz_sdk.orm_adapters.pynamodb import (
        PynamodbORMAdapter,
        sslcommerz_session_pynamodb_model_factory,
    )
    from sslcommerz_sdk.store import SslcommerzStore
    from sslcommerz_sdk.store_providers import SingleStoreProvider

    SslcommerzSession = sslcommerz_session_pynamodb_model_factory(region="us-east-1")
    store = SslcommerzStore(
        store_id="YOUR_STORE_ID",
        store_passwd="YOUR_STORE_PASSWORD",
        base_url="https://sandbox.sslcommerz.com",
    )
    payment_handler = PaymentHandler(
        model=SslcommerzSession,
        orm_adapter=PynamodbORMAdapter(),
        store_provider=SingleStoreProvider(store=store),
    )

You can customize the model with additional parameters to model factory.

.. code-block:: python

    SslcommerzSession = sslcommerz_session_pynamodb_model_factory(
        region="us-east-1",
        table_name="sslcommerz_sdk_session",
        read_capacity_units=1,
        write_capacity_units=1,
    )

Then you can create the model directly from a python shell prompt.

.. code-block:: python

    # Run in python shell
    from .payment_handler import SslcommerzSession
    SslcommerzSession.create_table()


When you are done, checkout `Next Steps`_.


.. _Next Steps: https://github.com/monim67/sslcommerz-sdk#next-steps
