from sslcommerz_sdk.enums import TransactionStatus
from sslcommerz_sdk.handlers import PaymentHandler
from sslcommerz_sdk.store import SslcommerzStore
from sslcommerz_sdk.testing import mock_sslcommerz_gateway


def test_valid_payment(store: SslcommerzStore, payment_handler: PaymentHandler):
    with mock_sslcommerz_gateway() as gateway:
        kwargs = gateway.generate_test_session_payload(store, "test")
        session, created = payment_handler.get_or_create_session(**kwargs)
        assert created
        test_payload = gateway.generate_valid_ipn_payload(
            store, session.tran_id, session.id
        )
        session, verified_right_now = payment_handler.verify_transaction(
            payload=test_payload
        )
        assert verified_right_now
        assert session.status == TransactionStatus.VALID


def test_failed_payment(store: SslcommerzStore, payment_handler: PaymentHandler):
    with mock_sslcommerz_gateway() as gateway:
        kwargs = gateway.generate_test_session_payload(store, "test")
        session, created = payment_handler.get_or_create_session(**kwargs)
        assert created
        test_payload = gateway.generate_failed_ipn_payload(
            store, session.tran_id, session.id
        )
        session, verified_right_now = payment_handler.verify_transaction(
            payload=test_payload
        )
        assert verified_right_now
        assert session.status == TransactionStatus.FAILED


def test_canceled_payment(store: SslcommerzStore, payment_handler: PaymentHandler):
    with mock_sslcommerz_gateway() as gateway:
        kwargs = gateway.generate_test_session_payload(store, "test")
        session, created = payment_handler.get_or_create_session(**kwargs)
        assert created
        test_payload = gateway.generate_canceled_ipn_payload(
            store, session.tran_id, session.id
        )
        session, verified_right_now = payment_handler.verify_transaction(
            payload=test_payload
        )
        assert verified_right_now
        assert session.status == TransactionStatus.CANCELLED


def test_unattempted_payment(store: SslcommerzStore, payment_handler: PaymentHandler):
    with mock_sslcommerz_gateway() as gateway:
        kwargs = gateway.generate_test_session_payload(store, "test")
        session, created = payment_handler.get_or_create_session(**kwargs)
        assert created
        test_payload = gateway.generate_unattempted_ipn_payload(
            store, session.tran_id, session.id
        )
        session, verified_right_now = payment_handler.verify_transaction(
            payload=test_payload
        )
        assert verified_right_now
        assert session.status == TransactionStatus.UNATTEMPTED
