from decouple import config
from benny_dealz.settings import DEBUG

if DEBUG:
    pstk_public_key = "pk_test_a693ff0d97fe8a3bdc599d3eae5fe3cd1d483a23"
    pstk_secret_key = "sk_test_6e669ad7155e5cc5acf6c4ff70760e947b9ee476"
else:
    pstk_public_key = config('LIVE_PSTK_PUBLIC_KEY')
    pstk_secret_key = config('LIVE_PSTK_SECRET_KEY')
