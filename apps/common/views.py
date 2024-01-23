import threading

import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException


def convert_to_true_or_false_v2(request, data):
    switch = request.POST.get(data, False)
    return switch == 'true'


def convert_import_to_true_or_false(data):
    if str(data) == "1" or data == 1:
        return True
    elif str(data) == "0" or data == 0:
        return False
    elif isinstance(data, str) and data.lower() in ["true", "yes"]:
        return True
    return False


def validate_phone_number(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number, None)
        return bool(phonenumbers.is_valid_number(parsed_number))
    except NumberParseException as e:
        print(e)
        return False


class EmailThreading(threading.Thread):
    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send(fail_silently=True)
