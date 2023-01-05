import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, Integer, Numeric, String, Text

from ..enums import TransactionStatus
from .base import AbstractORMAdapter


class SqlalchemyORMAdapter(AbstractORMAdapter):
    def __init__(self, db_session):
        self.db_session = db_session

    def get_session_instance_by_pk(self, model, pk):
        return self.db_session.query(model).get(pk)

    def get_session_instance_iterator(self, model, tran_id, status_list):
        query = self.db_session.query(model).filter(
            model.tran_id == tran_id, model.status.in_(status_list)
        )
        return iter(query)

    def save_session_instance(self, model, instance, **kwargs):
        self.db_session.add(instance)
        self.db_session.commit()


def sslcommerz_session_sqlalchemy_model_factory(base_class):
    class SslcommerzSession(base_class):
        __tablename__ = "sslcommerz_sdk_session"
        id = Column(String(36), primary_key=True, default=uuid.uuid4)
        sessionkey = Column(String(255), unique=True)
        tran_id = Column(String(255), nullable=False)
        store_id = Column(String(30), nullable=False)
        currency = Column(String(3), nullable=False)
        total_amount = Column(Numeric(10, 2), nullable=False)
        created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
        updated_at = Column(
            DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
        )
        status = Column(
            Enum(TransactionStatus, name="sslcommerz_sdk_session_status"),
            default=TransactionStatus.PENDING,
            nullable=False,
        )
        # Integration Parameters
        redirect_url = Column(String(255), nullable=False)
        multi_card_name = Column(String(255))
        allowed_bin = Column(String(255))
        # Customer Info
        cus_name = Column(String(50), nullable=False)
        cus_email = Column(String(50), nullable=False)
        cus_add1 = Column(String(50), nullable=False)
        cus_add2 = Column(String(50))
        cus_city = Column(String(50), nullable=False)
        cus_postcode = Column(String(50), nullable=False)
        cus_country = Column(String(50), nullable=False)
        cus_state = Column(String(50))
        cus_phone = Column(String(20), nullable=False)
        cus_fax = Column(String(20))
        # Shipment Information
        shipping_method = Column(String(50), nullable=False)
        num_of_item = Column(Integer)
        ship_name = Column(String(50))
        ship_add1 = Column(String(50))
        ship_add2 = Column(String(50))
        ship_city = Column(String(50))
        ship_state = Column(String(50))
        ship_postcode = Column(String(50))
        ship_country = Column(String(50))
        # Product Information
        product_name = Column(String(255), nullable=False)
        product_category = Column(String(100), nullable=False)
        product_profile = Column(String(100), nullable=False)
        hours_till_departure = Column(String(30))
        flight_type = Column(String(30))
        pnr = Column(String(50))
        journey_from_to = Column(String(255))
        third_party_booking = Column(String(20))
        hotel_name = Column(String(255))
        length_of_stay = Column(String(30))
        check_in_time = Column(String(30))
        hotel_city = Column(String(50))
        product_type = Column(String(30))
        topup_number = Column(String(150))
        country_topup = Column(String(30))
        cart = Column(Text)
        product_amount = Column(Numeric(10, 2))
        vat = Column(Numeric(10, 2))
        discount_amount = Column(Numeric(10, 2))
        convenience_fee = Column(Numeric(10, 2))
        # Parameters to Handle EMI Transaction
        emi_option = Column(Integer)
        emi_max_inst_option = Column(Integer)
        emi_selected_inst = Column(Integer)
        emi_allow_only = Column(Integer)
        # Additional Parameters
        value_a = Column(String(255))
        value_b = Column(String(255))
        value_c = Column(String(255))
        value_d = Column(String(255))
        # Payment Info
        val_id = Column(String(50))
        tran_date = Column(String(30))
        bank_tran_id = Column(String(80))
        currency_amount = Column(Numeric(10, 2))
        currency_rate = Column(Numeric(10, 2))
        currency_type = Column(String(3))
        amount = Column(Numeric(10, 2))
        currency = Column(String(3))
        store_amount = Column(Numeric(10, 2))
        card_type = Column(String(50))
        card_no = Column(String(80))
        card_issuer = Column(String(50))
        card_brand = Column(String(30))
        card_issuer_country = Column(String(50))
        card_issuer_country_code = Column(String(2))
        risk_level = Column(Integer)
        risk_title = Column(String(50))
        # Payloads
        ipn_payload = Column(Text)
        validation_response = Column(Text)

    return SslcommerzSession
