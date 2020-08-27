import enum
import hashlib
from contextlib import contextmanager
from requests.exceptions import RequestException

from .exceptions import SslcommerzException, SslcommerzRequestException


class ChoicesMeta(enum.EnumMeta):
    @property
    def choices(cls):
        return [(member.value, member.label) for member in cls]


class EnumChoice(str, enum.Enum, metaclass=ChoicesMeta):
    def __new__(cls, value, label=None):
        obj = str.__new__(cls, [value])
        obj._value_ = value
        obj.label = label or value
        return obj

    def __eq__(self, other):
        return str(self) == str(other)

    def __str__(self):
        return str(self.value)


class CustomFlagMixin:
    def __or__(self, other):
        return CustomFlag(f"{self},{other}")


class CustomFlag(CustomFlagMixin):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)


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


def validate_verify_sign(store_passwd, payload):
    verify_keys = payload["verify_key"].split(",")
    obj = {key: payload[key] for key in verify_keys}
    obj["store_passwd"] = hashlib.md5(store_passwd.encode()).hexdigest()
    hash_string = "&".join(f"{key}={obj[key]}" for key in sorted(obj.keys()))
    hash_string_md5 = hashlib.md5(hash_string.encode()).hexdigest()
    return hash_string_md5 == payload["verify_sign"]
