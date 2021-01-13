.. _setup-store:

####################
Setup Store
####################


`Register a sandbox account`_ for development purpose and set it up as below.

.. code-block:: python

    from sslcommerz_sdk.store import SslcommerzStore

    store = SslcommerzStore(
        store_id="YOUR_STORE_ID",
        store_passwd="YOUR_STORE_PASSWORD",
        base_url="https://sandbox.sslcommerz.com",
    )

For production create a marchant account on SSLCOMMERZ and set it up as below.

.. code-block:: python

    from sslcommerz_sdk.store import SslcommerzStore

    store = SslcommerzStore(
        store_id="YOUR_STORE_ID",
        store_passwd="YOUR_STORE_PASSWORD",
        base_url="https://securepay.sslcommerz.com",
    )


.. _customize-store:

********************
Customize Store
********************

You can customize the store with additional parameters for testing purpose.

.. code-block:: python

    from sslcommerz_sdk.store import SslcommerzStore

    store = SslcommerzStore(
        store_id="YOUR_STORE_ID",
        store_passwd="YOUR_STORE_PASSWORD",
        base_url="https://securepay.sslcommerz.com",
        session_url="/gwprocess/v4/api.php",
        validation_url="/validator/api/validationserverAPI.php",
        transaction_url="/validator/api/merchantTransIDvalidationAPI.php",
    )


.. _setup-multiple-store:

********************
Setup Multiple Store
********************

To handle more than one store use :code:`MultpleStoreProvider` instead in your payment handler.

.. code-block:: python

    from sslcommerz_sdk.store_providers import MultpleStoreProvider

    def get_store_by_id(store_id):
        # TODO: Retrieve password of the store by store_id
        return SslcommerzStore(
            store_id=store_id,
            store_passwd="PASSWORD of that store",
            base_url="https://sandbox.sslcommerz.com",
        )

    payment_handler = PaymentHandler(
        model="YOUR_MODEL",
        orm_adapter="YOUR_ORM_ADAPTER",
        store_provider=MultpleStoreProvider(get_store_by_id=get_store_by_id),
    )

When you are done, checkout `Next Steps`_.


.. _Register a sandbox account: https://developer.sslcommerz.com/registration/
.. _Next Steps: https://github.com/monim67/sslcommerz-sdk#next-steps
