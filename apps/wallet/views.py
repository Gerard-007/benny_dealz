from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.base import View
from apps.wallet.models import WalletTransactions, Wallet
from benny_dealz.third_parties.flutter_wave import secret_key, public_key
from apps.dealers.models import Dealer
from benny_dealz.third_parties.paystack import pstk_public_key


# class ValidateBVN(View):
#     def post(self, request):
#         data = json.loads(request.body)
#         bvn = data['bvn']
#         print(bvn)
#         if bvn.isnumeric():
#             if Wallet.objects.filter(bvn=bvn).exists():
#                 return JsonResponse({'bvn_error': "Sorry bvn already in use"})
#             url = f"https://api.flutterwave.com/v3/kyc/bvns/{bvn}"
#             payload = ""
#             sk = secret_key
#             headers = {
#                 'Authorization': f'Bearer {sk}'
#             }
#             response = requests.request("GET", url, headers=headers, data=payload)
#             print(response.text)
#             return JsonResponse({'bvn_valid': True})
#         elif len(bvn) > 11:
#             return JsonResponse({'bvn_length_invalid': "You bvn must not exceed 11 digits."})
#         return JsonResponse({'bvn_type_invalid': "Please enter a valid bvn must not contain letter"})


class WalletView(LoginRequiredMixin, View):
    template_name = "wallet/fund_wallet.html"

    def get(self, request, uid):
        wallet = Wallet.objects.filter(uid=uid).first()
        wallet_transactions = WalletTransactions.objects.filter(wallet=wallet)
        pub_key = public_key
        pstk_pub_key = pstk_public_key
        get_dealer = Dealer.objects.get(user=self.request.user)

        context = {
            "wallet": wallet,
            "pub_key": pub_key,
            "pstk_pub_key": pstk_pub_key,
            "get_dealer": get_dealer,
            "wallet_transactions": wallet_transactions
        }
        return render(request, self.template_name, context)


class FundWalletView(LoginRequiredMixin, View):

    def post(self, request, uid):
        get_currency = request.POST['currency']
        get_reference = request.POST['reference']
        get_amount = request.POST['amount']
        get_status = request.POST['status']
        wallet = Wallet.objects.get(uid=uid)
        user = self.request.user

        print(f"""
            get_currency: {get_currency}
            get_reference: {get_reference}
            get_amount: {get_amount}
            get_status: {get_status}
        """)

        wallet_transaction = WalletTransactions(
            wallet=wallet,
            transaction_id=get_reference,
            currency=get_currency,
            amount=get_amount,
            payment_status=get_status,
        )
        wallet_transaction.save()
        print("Wallet transactions updated")

        # Update wallet balance...
        wallet.balance = F('balance') + float(get_amount)
        wallet.save()
        print("Wallet Balance Updated")

        return JsonResponse({
            "status": "success",
            "message": "Transaction success & your wallet balance was updated."
        })

# Object {
#     status: "successful",
#     customer: {…},
#     transaction_id: 3344910,
#     tx_ref: "bnnydlz_ref-92673",
#     flw_ref: "FLW-M03K-9f7e65cb688b48bbcb3bd7cb7e5aaf7e",
#     currency: "NGN",
#     amount: 4000,
#     redirectstatus: undefined
# }

# var = {
#     "status": "success",
#     "message": "Virtual account created",
#     "data": {
#         "response_code": "02",
#         "response_message": "Transaction in progress",
#         "order_ref": "URF_1651463031274_7327235",
#         "account_number": "1234567890",
#         "bank_name": "TEST BANK",
#         "amount": "NaN"
#     }
# }

# {
#     "status":"error",
#     "message":"Merchant requires approval to use resource, please contact support",
#     "data":null
# }

# account_data = {
#     'status': 'success',
#     'message': 'Virtual account created',
#     'data': {
#         'response_code': '02',
#         'response_message': 'Transaction in progress',
#         'order_ref': 'URF_1651781636230_8889335',
#         'account_number': '1234567890',
#         'bank_name': 'TEST BANK',
#         'amount': 'NaN'
#     }
# }
