import json
import uuid
from datetime import datetime
from decimal import Decimal

from pynamodb.attributes import (
    NumberAttribute,
    UnicodeAttribute,
    UTCDateTimeAttribute,
)
from pynamodb.indexes import GlobalSecondaryIndex, KeysOnlyProjection
from pynamodb.models import Model

from ..enums import TransactionStatus
from .base import AbstractORMAdapter


class DecimalAttribute(NumberAttribute):
    def __init__(self, max_digits, decimal_places, **kwargs):
        self.max_digits = max_digits
        self.decimal_places = decimal_places
        super().__init__(**kwargs)

    def serialize(self, value):
        return str(round(value, self.decimal_places))

    def deserialize(self, value):
        return Decimal(json.loads(value))


class EnumAttribute(UnicodeAttribute):
    def __init__(self, values, **kwargs):
        self.values = values
        super().__init__(**kwargs)

    def serialize(self, value):
        if value not in self.values:
            raise ValueError(
                f"{self.attr_name} must be one of {self.values}, not '{value}'"
            )
        else:
            return str(value)


class PynamodbORMAdapter(AbstractORMAdapter):
    def get_session_instance_by_pk(self, model, pk):
        try:
            return model.get(pk)
        except model.DoesNotExist:
            return None

    def get_session_instance_iterator(self, model, tran_id, status_list):
        for status in status_list:
            for instance in model.tran_id_index.query(tran_id, model.status == status):
                yield instance


def sslcommerz_session_pynamodb_model_factory(
    region, table_name="sslcommerz_sdk_session", **kwargs
):
    options = {"region": region, "table_name": table_name, **kwargs}

    class TranIdIndex(GlobalSecondaryIndex):
        tran_id = UnicodeAttribute(hash_key=True)
        status = UnicodeAttribute(range_key=True)

        class Meta:
            projection = KeysOnlyProjection()
            read_capacity_units = options.get("read_capacity_units", 1)
            write_capacity_units = options.get("write_capacity_units", 1)

    class SslcommerzSession(Model):
        class Meta:
            region = options["region"]
            table_name = options["table_name"]
            read_capacity_units = options.get("read_capacity_units", 1)
            write_capacity_units = options.get("write_capacity_units", 1)

        id = UnicodeAttribute(hash_key=True, default_for_new=lambda: str(uuid.uuid4()))
        sessionkey = UnicodeAttribute()
        tran_id = UnicodeAttribute()
        tran_id_index = TranIdIndex()
        store_id = UnicodeAttribute()
        currency = UnicodeAttribute()
        total_amount = DecimalAttribute(max_digits=10, decimal_places=2)
        created_at = UTCDateTimeAttribute(default_for_new=datetime.utcnow)
        updated_at = UTCDateTimeAttribute(default=datetime.utcnow)
        status = EnumAttribute(
            values=[choice.value for choice in TransactionStatus],
            default=TransactionStatus.PENDING,
        )
        # Integration Parameters
        redirect_url = UnicodeAttribute()
        multi_card_name = UnicodeAttribute(null=True)
        allowed_bin = UnicodeAttribute(null=True)
        # Customer Info
        cus_name = UnicodeAttribute()
        cus_email = UnicodeAttribute()
        cus_add1 = UnicodeAttribute()
        cus_add2 = UnicodeAttribute(null=True)
        cus_city = UnicodeAttribute()
        cus_postcode = UnicodeAttribute()
        cus_country = UnicodeAttribute()
        cus_state = UnicodeAttribute(null=True)
        cus_phone = UnicodeAttribute()
        cus_fax = UnicodeAttribute(null=True)
        # Shipment Information
        shipping_method = UnicodeAttribute()
        num_of_item = NumberAttribute(null=True)
        ship_name = UnicodeAttribute(null=True)
        ship_add1 = UnicodeAttribute(null=True)
        ship_add2 = UnicodeAttribute(null=True)
        ship_city = UnicodeAttribute(null=True)
        ship_state = UnicodeAttribute(null=True)
        ship_postcode = UnicodeAttribute(null=True)
        ship_country = UnicodeAttribute(null=True)
        # Product Information
        product_name = UnicodeAttribute()
        product_category = UnicodeAttribute()
        product_profile = UnicodeAttribute()
        hours_till_departure = UnicodeAttribute(null=True)
        flight_type = UnicodeAttribute(null=True)
        pnr = UnicodeAttribute(null=True)
        journey_from_to = UnicodeAttribute(null=True)
        third_party_booking = UnicodeAttribute(null=True)
        hotel_name = UnicodeAttribute(null=True)
        length_of_stay = UnicodeAttribute(null=True)
        check_in_time = UnicodeAttribute(null=True)
        hotel_city = UnicodeAttribute(null=True)
        product_type = UnicodeAttribute(null=True)
        topup_number = UnicodeAttribute(null=True)
        country_topup = UnicodeAttribute(null=True)
        cart = UnicodeAttribute(null=True)
        product_amount = DecimalAttribute(max_digits=10, decimal_places=2, null=True)
        vat = DecimalAttribute(max_digits=10, decimal_places=2, null=True)
        discount_amount = DecimalAttribute(max_digits=10, decimal_places=2, null=True)
        convenience_fee = DecimalAttribute(max_digits=10, decimal_places=2, null=True)
        # Parameters to Handle EMI Transaction
        emi_option = NumberAttribute(null=True)
        emi_max_inst_option = NumberAttribute(null=True)
        emi_selected_inst = NumberAttribute(null=True)
        emi_allow_only = NumberAttribute(null=True)
        # Additional Parameters
        value_a = UnicodeAttribute(null=True)
        value_b = UnicodeAttribute(null=True)
        value_c = UnicodeAttribute(null=True)
        value_d = UnicodeAttribute(null=True)
        # Payment Info
        val_id = UnicodeAttribute(null=True)
        tran_date = UnicodeAttribute(null=True)
        bank_tran_id = UnicodeAttribute(null=True)
        currency_amount = DecimalAttribute(max_digits=10, decimal_places=2, null=True)
        currency_rate = DecimalAttribute(max_digits=10, decimal_places=2, null=True)
        currency_type = UnicodeAttribute(null=True)
        amount = DecimalAttribute(max_digits=10, decimal_places=2, null=True)
        currency = UnicodeAttribute(null=True)
        store_amount = DecimalAttribute(max_digits=10, decimal_places=2, null=True)
        card_type = UnicodeAttribute(null=True)
        card_no = UnicodeAttribute(null=True)
        card_issuer = UnicodeAttribute(null=True)
        card_brand = UnicodeAttribute(null=True)
        card_issuer_country = UnicodeAttribute(null=True)
        card_issuer_country_code = UnicodeAttribute(null=True)
        risk_level = NumberAttribute(null=True)
        risk_title = UnicodeAttribute(null=True)
        # Payloads
        ipn_payload = UnicodeAttribute(null=True)
        validation_response = UnicodeAttribute(null=True)

    return SslcommerzSession
