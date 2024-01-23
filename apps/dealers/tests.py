# @receiver(post_save, sender=Dealer)
# def create_wallet(sender, instance, created, **kwargs):
#     if created:
#         try:
#             sk = flutter_wave.secret_key
#             url = "https://api.flutterwave.com/v3/virtual-account-numbers"
#             payload = json.dumps({
#                 "email": instance.name.email,
#                 "bvn": instance.bvn,
#                 "narration": instance.business_name,
#                 "is_permanent": True
#             })
#             headers = {
#                 'Authorization': f'Bearer {sk}',
#                 'Content-Type': 'application/json'
#             }
#             response = requests.request("POST", url, headers=headers, data=payload)
#             va_data = response.json()
#             order_ref = va_data["data"]["order_ref"]
#             account_number = va_data["data"]["account_number"]
#             bank_name = va_data["data"]["bank_name"]
#             Wallet.objects.create(
#                 dealer=instance,
#                 bvn=instance.bvn,
#                 virtual_account_ref=order_ref,
#                 virtual_bank_name=bank_name,
#                 virtual_account_number=account_number
#             )
#         except Exception:
#             return redirect("/")
