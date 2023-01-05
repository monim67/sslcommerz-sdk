from requests.exceptions import RequestException


class SslcommerzException(IOError):
    """ An exception raised by sslcommerz_sdk app """

    def __init__(self, *args, **kwargs):
        self.tran_id = kwargs.pop("tran_id", None)
        super().__init__(*args, **kwargs)

    def __str__(self):
        error_str = super().__str__()
        return f"{error_str}, tran_id: {self.tran_id}"


class SslcommerzRequestException(SslcommerzException, RequestException):
    """ RequestException raised by requests library """


class SslcommerzAPIException(SslcommerzException):
    """ Unexpected response or explicit error response from sslcommerz api """


class SessionDoesNotExistException(SslcommerzException):
    """ Raised when a session does not exist in database """


class InvalidPaymentException(SslcommerzException):
    """ Raised when a IPN payload is invalid """


class TranIdReuseException(SslcommerzException):
    """
    Raised when a successful transaction ID is attempted to be reused.

    If your transaction fails you can attempt again using the same transaction ID,
    but if a transaction is successful you cannot reuse the same transaction ID later.
    An attempt to do so will raise this exception.
    """


class TotalAmountTamperedException(SslcommerzException):
    """
    Raised when total_amount changes when there is a pending payment going on.

    When user is redirected to Payment Gateway there is no stopping the transaction,
    you should freeze the basket before redirecting the user, the user should not be
    allowed to modify the basket that alters the total_amount to be paid by him
    (for example he cannot add/remove items from the basket or clear the basket).
    Only if the user cancels the transaction, or the transaction fails or expires,
    you should unfreeze the basket and let the user add/remove items to basket.
    """
