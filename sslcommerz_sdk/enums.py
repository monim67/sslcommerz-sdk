from .helpers import EnumChoice, CustomFlagMixin


class TransactionStatus(EnumChoice):
    INVALID = "INVALID"
    PENDING = "PENDING"
    VALIDATED = "VALIDATED"
    # IPN notification status
    VALID = "VALID"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    UNATTEMPTED = "UNATTEMPTED"
    EXPIRED = "EXPIRED"


class ProductProfile(EnumChoice):
    GENERAL = "general"
    PHYSICAL_GOODS = "physical-goods"
    NON_PHYSICAL_GOODS = "non-physical-goods"
    AIRLINE_TICKETS = "airline-tickets"
    TRAVEL_VERTICAL = "travel-vertical"
    TELECOM_VERTICAL = "telecom-vertical"


class MultiCardName(CustomFlagMixin, EnumChoice):
    BRAC_VISA = "brac_visa", "BRAC VISA"
    DBBL_VISA = "dbbl_visa", "Dutch Bangla VISA"
    CITY_VISA = "city_visa", "City Bank Visa"
    EBL_VISA = "ebl_visa", "EBL Visa"
    SBL_VISA = "sbl_visa", "Southeast Bank Visa"
    BRAC_MASTER = "brac_master", "BRAC MASTER"
    DBBL_MASTER = "dbbl_master", "MASTER Dutch-Bangla"
    CITY_MASTER = "city_master", "City Master Card"
    EBL_MASTER = "ebl_master", "EBL Master Card"
    SBL_MASTER = "sbl_master", "Southeast Bank Master Card"
    CITY_AMEX = "city_amex", "City Bank AMEX"
    QCASH = "qcash", "QCash"
    DBBL_NEXUS = "dbbl_nexus", "DBBL Nexus"
    BANKASIA = "bankasia", "Bank Asia IB"
    ABBANK = "abbank", "AB Bank IB"
    IBBL = "ibbl", "IBBL IB and Mobile Banking"
    MTBL = "mtbl", "Mutual Trust Bank IB"
    BKASH = "bkash", "Bkash Mobile Banking"
    DBBLMOBILEBANKING = "dbblmobilebanking", "DBBL Mobile Banking"
    CITY = "city", "City Touch IB"
    UPAY = "upay", "Upay"
    TAPNPAY = "tapnpay", "Tap N Pay Gateway"
    INTERNETBANK = "internetbank", "For all internet banking"
    MOBILEBANK = "mobilebank", "For all mobile banking"
    OTHERCARD = "othercard", "For all cards except visa, master and amex"
    VISACARD = "visacard", "For all visa"
    MASTERCARD = "mastercard", "For All Master card"
    AMEXCARD = "amexcard", "For Amex Card"
