from django import forms
from django.core.mail import send_mail
import logging
from django.forms import inlineformset_factory
from . import models
from . import widgets
from localusers.models import Address

logger = logging.getLogger(__name__)


class ContactForm(forms.Form):
    name = forms.CharField(label='Your Name ', max_length=100, required=True)
    message = forms.CharField(
        max_length=600, widget=forms.Textarea, required=True)

    def send_mail(self):
        logger.info('Sending email to customer service')
        message = f"From:{self.cleaned_data['name']}, Message: {self.cleaned_data['message']}"
        send_mail(
            'Site Message',
            message,
            'site@booktime.domain',
            ["customerservice@booktime.domain"],
            fail_silently=False,
        )


BasketLineFormSet = inlineformset_factory(
    models.Basket,
    models.BasketLine,
    fields=("quantity",),
    extra=0,
    widgets={"quantity": widgets.PlusMinusNumberInput()},
)


class AddressSelectionForm(forms.Form):
    billing_address = forms.ModelChoiceField(queryset=None)
    shipping_address = forms.ModelChoiceField(queryset=None)

    def __init__(self, user, *args, **kwargs):
        super(). __init__(*args, **kwargs)
        queryset = Address.objects.filter(user=user)
        self.fields['billing_address'].queryset = queryset
        self.fields['shipping_address'].queryset = queryset
