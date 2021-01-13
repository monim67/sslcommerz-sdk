from django.http import JsonResponse
from django.views.generic import View


class SessionCreateView(View):
    def post(self, request, *args, **kwargs):
        return JsonResponse({
            "status": "SUCCESS",
            "failedreason": "",
            "sessionkey": "SESSION0",
            "GatewayPageURL": "https://sandbox.sslcommerz.com/EasyCheckOut/test",
            "storeBanner": "https://sandbox.sslcommerz.com/stores/logos/demoLogo.png",
            "storeLogo": "https://sandbox.sslcommerz.com/stores/logos/demoLogo.png",
            "store_name": "Demo",
        })


class TransactionValidationView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({
            "status": "VALIDATED",
            "tran_date": "2020-12-28 18:14:09",
            "tran_id": "test01",
            "val_id": "val_id",
            "amount": "100.00",
            "store_amount": "97.5",
            "currency": "BDT",
            "bank_tran_id": "bank_tran_id",
            "currency_type": "BDT",
            "currency_amount": "100.00",
            "currency_rate": "1.0000",
            "base_fair": "0.00",
            "value_a": "",
            "value_b": "",
            "value_c": "",
            "value_d": "2561e69e-be76-4f2c-a665-2bd3af76b62c",
            "account_details": "",
            "risk_title": "Safe",
            "risk_level": "0",
            "APIConnect": "DONE",
            "validated_on": "2020-12-28 18:19:11",
            "gw_version": "",
            "offer_avail": 1,
            "isTokeizeSuccess": 0,
            "campaign_code": ""
        })
