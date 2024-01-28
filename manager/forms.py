from django import forms
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _

from .models import ChargePoint


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
