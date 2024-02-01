from django import forms
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _

from .models import ChargePoint, Transaction, TransactionStatus


class ChargePointAdminForm(forms.ModelForm):
    password = forms.CharField(label=_('New Password'), required=False, widget=forms.PasswordInput)

    class Meta:
        model = ChargePoint
        fields = '__all__'

    def save(self, commit=True):
        instance = super().save(commit=False)
        password = self.cleaned_data.get('password')

        if password:
            instance.password_hash = make_password(password)

        if commit:
            instance.save()

        return instance


class RemoteStartTransactionForm(forms.Form):
    charge_point = forms.ModelChoiceField(queryset=ChargePoint.objects.all())

    connector_id = forms.IntegerField(label=_('Connector ID'), required=True)

    vehicle = forms.CharField(label=_('Vehicle'), required=False)

    address = forms.CharField(label=_('Address'), required=False)

    city = forms.CharField(label=_('City'), required=False)

    external_id = forms.CharField(label=_('External ID'), required=False)


class RemoteStopTransactionForm(forms.Form):
    transaction = forms.ModelChoiceField(
        queryset=Transaction.objects.filter(
            status__in=[
                TransactionStatus.started.value,
                TransactionStatus.stopping.value,
            ]
        )
    )
