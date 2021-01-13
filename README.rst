######
|logo|
######

|  |build-status| |docs-status| |coverage|
|  |pyversions| |pypi-version| |license|


Python SDK for SSLCOMMERZ configurable with Sqlalchemy, PynamoDB or Django ORM.


********************
Getting Started
********************

Install it via pip (python>=3.0).

.. code:: text

    pip install sslcommerz-sdk


********************
How to Use
********************

Create the views below depending on framework you are using.

.. code:: python

    from sslcommerz_sdk.enums import TransactionStatus

    # TODO: create payment_handler.py file
    from .payment_handler import payment_handler, store


    def payment_init_view():
        # TODO: Freeze the cart, see what cart freezing is
        session, created = payment_handler.get_or_create_session(
            store=store,
            tran_id="test",
            currency="BDT",
            total_amount=100,
            cus_name="test",
            cus_email="test@test.com",
            cus_add1="test",
            cus_city="test",
            cus_postcode="1234",
            cus_country="test",
            cus_phone="123456",
            success_url="<URL to redirect cutomer when transaction is successful>",
            fail_url="<URL to redirect cutomer when transaction is failed>",
            cancel_url="<URL to redirect cutomer when transaction is cancelled>",
            ipn_url="<URL of ipn_view>",
        )
        # TODO: Redirect customer to session.redirect_url


    def ipn_view():
        # TODO: Make this URL public, i.e accessible without logging in
        # TODO: Disable CSRF protection for this view
        # TODO: post_dict = {dict of request POST values}
        session, verified_right_now = payment_handler.verify_transaction(
            payload=post_dict,
        )
        if verified_right_now:
            if session.status == TransactionStatus.VALID:
                print(f"Tran ID: {session.tran_id} successful...")
                # TODO: Update order payment status in your database
            else:
                print("Transaction failed/cancelled!")
                # TODO: Unfreeze the cart sothat customer can modify/delete the cart


********************
Next Steps
********************

- Setup Payment Handler with any of the following ORM.
    - `Django ORM <https://sslcommerz-sdk.readthedocs.io/en/latest/setup-payment-handler.html#django-orm>`_.
    - `Sqlalchemy <https://sslcommerz-sdk.readthedocs.io/en/latest/setup-payment-handler.html#sqlalchemy>`_.
    - `PynamoDB <https://sslcommerz-sdk.readthedocs.io/en/latest/setup-payment-handler.html#pynamodb>`_.
- `Setup Store <https://sslcommerz-sdk.readthedocs.io/en/latest/setup-store.html#setup-store>`_.
- `Configure Multiple Stores <https://sslcommerz-sdk.readthedocs.io/en/latest/setup-store.html#setup-multiple-store>`_.
- `Customize Store <https://sslcommerz-sdk.readthedocs.io/en/latest/setup-store.html#customize-store>`_.
- `Create Sandbox Account <https://developer.sslcommerz.com/registration/>`_.
- `Checkout SSLCOMMERZ api documentation <https://developer.sslcommerz.com/doc/v4/>`_.
- `Freeze shopping cart to avoid unexpected errors <https://sslcommerz-sdk.readthedocs.io/en/latest/best-practices.html#freeze-your-cart>`_.


********************
Contributing
********************

PR should pass the tests and lint commands, checkout the following to get started.

- `CONTRIBUTING.md <https://github.com/monim67/sslcommerz-sdk/blob/master/.github/CONTRIBUTING.md>`_.
- `CODE_OF_CONDUCT.md <https://github.com/monim67/sslcommerz-sdk/blob/master/.github/CODE_OF_CONDUCT.md>`_.


********************
License
********************

This project is published under `MIT LICENSE <https://github.com/monim67/sslcommerz-sdk/blob/master/LICENSE>`_.


.. |logo| image:: https://raw.githubusercontent.com/monim67/sslcommerz-sdk/c339311f86d4d1943c0b173734323c3f0ef48a36/.github/assets/logo.png
    :width: 400px
    :height: 68px
    :alt: sslcommerz-sdk

.. |build-status| image:: https://github.com/monim67/sslcommerz-sdk/workflows/build/badge.svg
    :target: https://github.com/monim67/sslcommerz-sdk/actions?query=build
    :alt: Build Status
    :height: 20px

.. |docs-status| image:: https://readthedocs.org/projects/sslcommerz-sdk/badge/?version=latest
    :target: https://sslcommerz-sdk.readthedocs.io/en/latest/?badge=latest
    :alt: Docs Build Status
    :height: 20px

.. |coverage| image:: https://coveralls.io/repos/github/monim67/sslcommerz-sdk/badge.svg?branch=master
    :target: https://coveralls.io/github/monim67/sslcommerz-sdk?branch=master
    :alt: Coverage
    :height: 20px

.. |pyversions| image:: https://img.shields.io/pypi/pyversions/sslcommerz-sdk.svg
    :target: https://pypi.python.org/pypi/sslcommerz-sdk
    :alt: Python Versions
    :height: 20px

.. |pypi-version| image:: https://badge.fury.io/py/sslcommerz-sdk.svg
    :target: https://pypi.python.org/pypi/sslcommerz-sdk
    :alt: PyPI Version
    :height: 20px

.. |license| image:: https://img.shields.io/pypi/l/sslcommerz-sdk.svg
    :target: https://github.com/monim67/sslcommerz-sdk/blob/master/LICENSE
    :alt: MIT Licence
    :height: 20px
