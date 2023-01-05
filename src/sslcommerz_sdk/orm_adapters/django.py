import uuid

from django.db import models

from ..enums import TransactionStatus
from .base import AbstractORMAdapter


class DjangoORMAdapter(AbstractORMAdapter):
    def get_session_instance_by_pk(self, model, pk):
        return model.objects.filter(pk=pk).first()

    def get_session_instance_iterator(self, model, tran_id, status_list):
        return iter(model.objects.filter(tran_id=tran_id, status__in=status_list))


class AbstractSslcommerzSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    sessionkey = models.CharField(max_length=50, unique=True)
    tran_id = models.CharField(max_length=255)
    store_id = models.CharField(max_length=30)
    currency = models.CharField(max_length=3)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20,
        choices=TransactionStatus.get_choices(),
        default=TransactionStatus.PENDING,
    )
    # Integration Parameters
    redirect_url = models.CharField(max_length=255)
    multi_card_name = models.CharField(max_length=255, null=True)
    allowed_bin = models.CharField(max_length=255, null=True)
    # Customer Info
    cus_name = models.CharField(max_length=50)
    cus_email = models.CharField(max_length=50)
    cus_add1 = models.CharField(max_length=50)
    cus_add2 = models.CharField(max_length=50, null=True)
    cus_city = models.CharField(max_length=50)
    cus_postcode = models.CharField(max_length=50)
    cus_country = models.CharField(max_length=50)
    cus_state = models.CharField(max_length=50, null=True)
    cus_phone = models.CharField(max_length=20)
    cus_fax = models.CharField(max_length=20, null=True)
    # Shipment Information
    shipping_method = models.CharField(max_length=50)
    num_of_item = models.PositiveIntegerField(null=True)
    ship_name = models.CharField(max_length=50, null=True)
    ship_add1 = models.CharField(max_length=50, null=True)
    ship_add2 = models.CharField(max_length=50, null=True)
    ship_city = models.CharField(max_length=50, null=True)
    ship_state = models.CharField(max_length=50, null=True)
    ship_postcode = models.CharField(max_length=50, null=True)
    ship_country = models.CharField(max_length=50, null=True)
    # Product Information
    product_name = models.CharField(max_length=255)
    product_category = models.CharField(max_length=100)
    product_profile = models.CharField(max_length=100)
    hours_till_departure = models.CharField(max_length=30, null=True)
    flight_type = models.CharField(max_length=30, null=True)
    pnr = models.CharField(max_length=50, null=True)
    journey_from_to = models.CharField(max_length=255, null=True)
    third_party_booking = models.CharField(max_length=20, null=True)
    hotel_name = models.CharField(max_length=255, null=True)
    length_of_stay = models.CharField(max_length=30, null=True)
    check_in_time = models.CharField(max_length=30, null=True)
    hotel_city = models.CharField(max_length=50, null=True)
    product_type = models.CharField(max_length=30, null=True)
    topup_number = models.CharField(max_length=150, null=True)
    country_topup = models.CharField(max_length=30, null=True)
    cart = models.TextField(null=True)
    product_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    vat = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    convenience_fee = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    # Parameters to Handle EMI Transaction
    emi_option = models.PositiveIntegerField(null=True)
    emi_max_inst_option = models.PositiveIntegerField(null=True)
    emi_selected_inst = models.PositiveIntegerField(null=True)
    emi_allow_only = models.PositiveIntegerField(null=True)
    # Additional Parameters
    value_a = models.CharField(max_length=255, null=True)
    value_b = models.CharField(max_length=255, null=True)
    value_c = models.CharField(max_length=255, null=True)
    value_d = models.CharField(max_length=255, null=True)
    # Payment Info
    val_id = models.CharField(max_length=50, null=True)
    tran_date = models.CharField(max_length=30, null=True)
    bank_tran_id = models.CharField(max_length=80, null=True)
    currency_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    currency_rate = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    currency_type = models.CharField(max_length=3, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    currency = models.CharField(max_length=3, null=True)
    store_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    card_type = models.CharField(max_length=50, null=True)
    card_no = models.CharField(max_length=80, null=True)
    card_issuer = models.CharField(max_length=50, null=True)
    card_brand = models.CharField(max_length=30, null=True)
    card_issuer_country = models.CharField(max_length=50, null=True)
    card_issuer_country_code = models.CharField(max_length=2, null=True)
    risk_level = models.PositiveIntegerField(null=True)
    risk_title = models.CharField(max_length=50, null=True)
    # Payloads
    ipn_payload = models.TextField(null=True)
    validation_response = models.TextField(null=True)

    class Meta:
        abstract = True
