import hashlib
import json
import re
from contextlib import contextmanager
from typing import Iterator

import responses

from .store import DEFAULT_CONFIG, SslcommerzStore

DEFAULT_KWARGS = dict(
    cus_name="test",
    cus_email="test@test.com",
    cus_add1="test",
    cus_city="test",
    cus_postcode="1234",
    cus_country="test",
    cus_phone="123456",
    currency="BDT",
    total_amount=100,
    ipn_url="",
    success_url="",
    fail_url="",
    cancel_url="",
)


@contextmanager
def mock_sslcommerz_gateway() -> Iterator["MockGateway"]:
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add_callback(
            responses.POST,
            re.compile(
                "https://(sandbox|securepay).sslcommerz.com"
                + DEFAULT_CONFIG["session_url"]
            ),
            callback=session_request_callback,
            content_type="application/json",
        )
        rsps.add_callback(
            responses.GET,
            re.compile(
                "https://(sandbox|securepay).sslcommerz.com"
                + DEFAULT_CONFIG["validation_url"]
            ),
            callback=validation_request_callback,
            content_type="application/json",
        )
        yield MockGateway()


def session_request_callback(request):
    resp_body = {
        "status": "SUCCESS",
        "failedreason": "",
        "sessionkey": "SESSION0",
        "GatewayPageURL": "https://sandbox.sslcommerz.com/EasyCheckOut/test",
        "storeBanner": "https://sandbox.sslcommerz.com/stores/logos/demoLogo.png",
        "storeLogo": "https://sandbox.sslcommerz.com/stores/logos/demoLogo.png",
        "store_name": "Demo",
    }
    return (200, {}, json.dumps(resp_body))


def validation_request_callback(request):
    resp_body = {
        "status": "VALIDATED",
        "tran_date": "2020-12-28 18:14:09",
        "tran_id": "test01",
        "val_id": "val_id",
        "amount": "100.00",
        "store_amount": "97.5",
        "currency": "BDT",
        "bank_tran_id": "bank_tran_id",
        "currency_type": "BDT",
        "currency_amount": "100.00",
        "currency_rate": "1.0000",
        "base_fair": "0.00",
        "value_a": "",
        "value_b": "",
        "value_c": "",
        "value_d": "2561e69e-be76-4f2c-a665-2bd3af76b62c",
        "account_details": "",
        "risk_title": "Safe",
        "risk_level": "0",
        "APIConnect": "DONE",
        "validated_on": "2020-12-28 18:19:11",
        "gw_version": "",
        "offer_avail": 1,
        "isTokeizeSuccess": 0,
        "campaign_code": "",
    }
    return (200, {}, json.dumps(resp_body))


class MockGateway:
    def generate_test_session_payload(self, store: SslcommerzStore, tran_id: str):
        return dict(
            store=store,
            tran_id=tran_id,
            cus_name="test",
            cus_email="test@test.com",
            cus_add1="test",
            cus_city="test",
            cus_postcode="1234",
            cus_country="test",
            cus_phone="123456",
            currency="BDT",
            total_amount=100,
            ipn_url="",
            success_url="",
            fail_url="",
            cancel_url="",
        )

    def generate_valid_ipn_payload(
        self, store: SslcommerzStore, tran_id: str, session_id: str
    ):
        return self._sign_ipn_payload(
            store,
            {
                "tran_id": tran_id,
                "val_id": "201228181905yY5TDTXd3Xc7aWi",
                "amount": "100.00",
                "card_type": "VISA-Dutch Bangla",
                "store_amount": "97.50",
                "card_no": "455445XXXXXX4326",
                "bank_tran_id": "2012281819050EKvRpPgPpY3eDG",
                "status": "VALID",
                "tran_date": "2020-12-28 18:14:09",
                "error": "",
                "currency": "BDT",
                "card_issuer": "STANDARD CHARTERED BANK",
                "card_brand": "VISA",
                "card_sub_brand": "Classic",
                "card_issuer_country": "Bangladesh",
                "card_issuer_country_code": "BD",
                "store_id": "store_id",
                "currency_type": "BDT",
                "currency_amount": "100.00",
                "currency_rate": "1.0000",
                "base_fair": "0.00",
                "value_a": "",
                "value_b": "",
                "value_c": "",
                "value_d": session_id,
                "risk_level": "0",
                "risk_title": "Safe",
            },
        )

    def generate_failed_ipn_payload(
        self, store: SslcommerzStore, tran_id: str, session_id: str
    ):
        return self._sign_ipn_payload(
            store,
            {
                "tran_id": tran_id,
                "error": "Invalid expiration date",
                "status": "FAILED",
                "bank_tran_id": "200423152934IlNsxFzaZ6REpBO",
                "currency": "BDT",
                "tran_date": "2020-04-23 15:29:18",
                "amount": "100.00",
                "store_id": "store_id",
                "card_type": "",
                "card_no": "",
                "card_issuer": "",
                "card_brand": "",
                "card_sub_brand": "Classic",
                "card_issuer_country": "",
                "card_issuer_country_code": "",
                "currency_type": "BDT",
                "currency_amount": "100.00",
                "currency_rate": "1.0000",
                "base_fair": "0.00",
                "value_a": "",
                "value_b": "",
                "value_c": "",
                "value_d": session_id,
            },
        )

    def generate_canceled_ipn_payload(
        self, store: SslcommerzStore, tran_id: str, session_id: str
    ):
        return self._sign_ipn_payload(
            store,
            {
                "tran_id": tran_id,
                "status": "CANCELLED",
                "error": "Cancelled by User",
                "bank_tran_id": "",
                "currency": "BDT",
                "tran_date": "2020-04-23 15:36:14",
                "amount": "100.00",
                "store_id": "store_id",
                "currency_type": "BDT",
                "currency_amount": "100.00",
                "currency_rate": "1.0000",
                "base_fair": "0.00",
                "value_a": "",
                "value_b": "",
                "value_c": "",
                "value_d": session_id,
            },
        )

    def generate_unattempted_ipn_payload(
        self, store: SslcommerzStore, tran_id: str, session_id: str
    ):
        return self._sign_ipn_payload(
            store,
            {
                "tran_id": tran_id,
                "amount": "100.00",
                "bank_tran_id": "",
                "base_fair": "0.00",
                "card_brand": "",
                "card_issuer": "",
                "card_issuer_country": "",
                "card_issuer_country_code": "",
                "card_no": "",
                "card_sub_brand": "",
                "card_type": "",
                "currency": "BDT",
                "currency_amount": "100.00",
                "currency_rate": "1.0000",
                "currency_type": "BDT",
                "error": "Customer did not choose to pay any channel",
                "risk_level": "0",
                "risk_title": "Safe",
                "status": "UNATTEMPTED",
                "store_amount": "",
                "store_id": "qurbanibengalmeatlive",
                "tran_date": "2020-07-03 14:20:21",
                "val_id": "",
                "value_a": "",
                "value_b": "",
                "value_c": "",
                "value_d": session_id,
            },
        )

    def _sign_ipn_payload(self, store: SslcommerzStore, payload):
        obj = {
            **payload,
            "store_passwd": hashlib.md5(
                store.credentials["store_passwd"].encode()
            ).hexdigest(),
        }
        hash_string = "&".join(f"{key}={obj[key]}" for key in sorted(obj.keys()))
        hash_string_md5 = hashlib.md5(hash_string.encode()).hexdigest()
        return {
            **payload,
            "verify_sign": hash_string_md5,
            "verify_key": ",".join(payload.keys()),
            "verify_sign_sha2": "",
        }
