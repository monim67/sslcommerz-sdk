from abc import ABC, abstractmethod


class AbstractORMAdapter(ABC):
    def create_session_instance(self, model, **kwargs):
        return model(**kwargs)

    @abstractmethod
    def get_session_instance_by_pk(self, model, pk):
        pass

    @abstractmethod
    def get_session_instance_iterator(self, model, tran_id, status_list):
        pass

    def save_session_instance(self, model, instance, **kwargs):
        instance.save()


model_fields = {
    "tran_id",
    "store_id",
    "currency",
    "total_amount",
    "multi_card_name",
    "allowed_bin",
    "cus_name",
    "cus_email",
    "cus_add1",
    "cus_add2",
    "cus_city",
    "cus_postcode",
    "cus_country",
    "cus_state",
    "cus_phone",
    "cus_fax",
    "shipping_method",
    "num_of_item",
    "ship_name",
    "ship_add1",
    "ship_add2",
    "ship_city",
    "ship_state",
    "ship_postcode",
    "ship_country",
    "product_name",
    "product_category",
    "product_profile",
    "hours_till_departure",
    "flight_type",
    "pnr",
    "journey_from_to",
    "third_party_booking",
    "hotel_name",
    "length_of_stay",
    "check_in_time",
    "hotel_city",
    "product_type",
    "topup_number",
    "country_topup",
    "cart",
    "product_amount",
    "vat",
    "discount_amount",
    "convenience_fee",
    "emi_option",
    "emi_max_inst_option",
    "emi_selected_inst",
    "emi_allow_only",
    "value_a",
    "value_b",
    "value_c",
    "value_d",
}
