import hashlib


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


def append_verify_sign(store_passwd, payload):
    obj = {**payload, "store_passwd": hashlib.md5(store_passwd.encode()).hexdigest()}
    hash_string = "&".join(f"{key}={obj[key]}" for key in sorted(obj.keys()))
    hash_string_md5 = hashlib.md5(hash_string.encode()).hexdigest()
    return {
        **payload,
        "verify_sign": hash_string_md5,
        "verify_key": ",".join(payload.keys()),
        "verify_sign_sha2": "",
    }


def generate_test_payload(session_id, store_passwd):
    return append_verify_sign(
        store_passwd=store_passwd,
        payload={
            "tran_id": "valid_transaction",
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
            "value_d": str(session_id),
            "risk_level": "0",
            "risk_title": "Safe",
        },
    )
