import requests

from .enums import TransactionStatus
from .exceptions import InvalidPaymentException, SslcommerzAPIException
from .services import PayloadSchema, is_verify_sign_valid


DEFAULT_CONFIG = {
    "base_url": "https://sandbox.sslcommerz.com",
    "session_url": "/gwprocess/v4/api.php",
    "validation_url": "/validator/api/validationserverAPI.php",
    "transaction_url": "/validator/api/merchantTransIDvalidationAPI.php",
}


class SslcommerzStore:
    def __init__(self, store_id, store_passwd, **kwargs):
        self.id = store_id
        self.credentials = dict(store_id=store_id, store_passwd=store_passwd)
        self.config = {**DEFAULT_CONFIG, **kwargs}

    def request(self, method, url, **kwargs):
        url = self.config["base_url"] + url
        return requests.request(method, url, **kwargs)

    def create_session(self, **kwargs):
        response = self.request(
            method="POST",
            url=self.config["session_url"],
            data={**self.credentials, **kwargs},
        )
        if response.status_code != 200:
            raise SslcommerzAPIException(
                f"Unexpected status code: {response.status_code}"
            )
        response_json = response.json()
        if response_json["status"] != "SUCCESS":
            raise SslcommerzAPIException(f"Error: {response_json['failedreason']}")
        return response_json

    def validate_ipn_payload(self, payload):
        try:
            if not is_verify_sign_valid(
                store_passwd=self.credentials["store_passwd"],
                payload=payload["original"],
            ):
                raise InvalidPaymentException("verify_sign mismatch")
            if payload["status"] == TransactionStatus.VALID:
                validation_response = self.validate_transaction(payload["val_id"])
                if validation_response["status"] not in (
                    TransactionStatus.VALID,
                    TransactionStatus.VALIDATED,
                ):
                    raise InvalidPaymentException(
                        f"Payment status: {validation_response['status']}"
                    )
                return PayloadSchema().load(validation_response)
        except KeyError as key:
            raise InvalidPaymentException(f"{key} is missing in payload") from key

    def validate_transaction(self, val_id):
        response = self.request(
            method="GET",
            url=self.config["validation_url"],
            params=dict(**self.credentials, val_id=val_id, format="json"),
        )
        if response.status_code != 200:
            raise SslcommerzAPIException(
                f"Unexpected status code: {response.status_code}"
            )
        return response.json()

    def query_transaction_by_sessionkey(self, sessionkey):
        response = self.request(
            method="GET",
            url=self.config["transaction_url"],
            params=dict(**self.credentials, sessionkey=sessionkey, format="json"),
        )
        return response.json()

    def query_transaction_by_tran_id(self, tran_id):
        response = self.request(
            method="GET",
            url=self.config["transaction_url"],
            params=dict(**self.credentials, tran_id=tran_id, format="json"),
        )
        return response.json()

    def init_refund(self, bank_tran_id, refund_amount, refund_remarks):
        response = self.request(
            method="GET",
            url=self.config["transaction_url"],
            params=dict(
                **self.credentials,
                bank_tran_id=bank_tran_id,
                refund_amount=refund_amount,
                refund_remarks=refund_remarks,
                format="json",
            ),
        )
        return response.json()

    def query_refund_status(self, refund_ref_id):
        response = self.request(
            method="GET",
            url=self.config["transaction_url"],
            params=dict(**self.credentials, refund_ref_id=refund_ref_id, format="json"),
        )
        return response.json()
