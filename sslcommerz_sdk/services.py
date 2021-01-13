import hashlib
import json
from contextlib import contextmanager

from marshmallow import INCLUDE, Schema, fields, pre_load
from requests.exceptions import RequestException

from .exceptions import (
    SslcommerzException,
    SslcommerzRequestException,
)


class PayloadSchema(Schema):
    amount = fields.Decimal(places=2)
    base_fair = fields.Decimal(places=2)
    currency_amount = fields.Decimal(places=2)
    currency_rate = fields.Decimal(places=4)
    store_amount = fields.Decimal(places=2)
    discount_amount = fields.Decimal(places=2)
    emi_amount = fields.Decimal(places=2)
    emi_instalment = fields.Int()
    risk_level = fields.Int()

    class Meta:
        unknown = INCLUDE

    @pre_load
    def envelope(self, in_data, **kwargs):
        return {**in_data, "original": in_data, "json": json.dumps(in_data)}


@contextmanager
def sslcommerz_exception_context(tran_id):
    """ Map all exceptions to SslcommerzException with provided tran_id. """
    if not tran_id:
        raise SslcommerzException("No tran_id provided")
    try:
        yield
    except SslcommerzException as ex:
        ex.tran_id = tran_id
        raise
    except RequestException as ex:
        raise SslcommerzRequestException(ex, tran_id=tran_id) from ex
    except Exception as ex:
        raise SslcommerzException(ex, tran_id=tran_id) from ex


def is_verify_sign_valid(store_passwd, payload):
    verify_keys = payload["verify_key"].split(",")
    obj = {key: payload[key] for key in verify_keys}
    obj["store_passwd"] = hashlib.md5(store_passwd.encode()).hexdigest()
    hash_string = "&".join(f"{key}={obj[key]}" for key in sorted(obj.keys()))
    hash_string_md5 = hashlib.md5(hash_string.encode()).hexdigest()
    return hash_string_md5 == payload["verify_sign"]
