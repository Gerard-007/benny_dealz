from django.forms import ModelForm
from apps.dealers.models import Dealer


class DealerForm(ModelForm):
    class Meta:
        model = Dealer
        fields = [
            'business_name',
            # 'business_email',
            # 'business_phone',
            'business_logo',
        ]
