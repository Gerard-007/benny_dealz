from decouple import config

from benny_dealz.settings import DEBUG

if DEBUG:
    public_key = "FLWPUBK_TEST-9e9d3b7b0391bdba2b3bfca818086862-X"
    secret_key = "FLWSECK_TEST-13f82f9409028db463aa494375ff8101-X"
    encryption_key = "FLWSECK_TESTdb601763b0ea"
else:
    public_key = config('LIVE_PUBLIC_KEY')
    secret_key = config('LIVE_SECRET_KEY')
    encryption_key = config('LIVE_ENCRYPTION_KEY')
