from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import FormView
from ocpp.v16.enums import ChargePointStatus
from rest_framework import serializers

from manager.forms import RemoteStartTransactionForm
from manager.models import ChargePoint
from manager.transactions import create_remote_transaction


class RemoteStartTransactionView(FormView):
    template_name = 'remote_start_transaction.html'
    form_class = RemoteStartTransactionForm

    def get_initial(self):
        initial = super().get_initial()
        charge_point_id = self.request.GET.get('charge_point')
        if charge_point_id:
            charge_point = get_object_or_404(ChargePoint, pk=charge_point_id)
        else:
            charge_point = ChargePoint.objects.filter(is_enabled=True, status=ChargePointStatus.available.value).first()

        if not charge_point:
            return initial

        initial['charge_point'] = charge_point
        initial['connector_id'] = 1
        initial['vehicle'] = 'Unknown'
        initial['city'] = charge_point.location.city if charge_point.location else 'Unknown'
        initial['address'] = charge_point.location.address1 if charge_point.location else 'Unknown'

        return initial

    def form_valid(self, form):
        data = form.cleaned_data
        try:
            transaction = create_remote_transaction(
                charge_point=data['charge_point'],
                connector_id=data['connector_id'],
                vehicle=data.get('vehicle') or 'Unknown',
                city=data.get('city') or data['charge_point'].location.city if data[
                    'charge_point'].location else 'Unknown',
                address=data.get('address') or data['charge_point'].location.address1 if data[
                    'charge_point'].location else 'Unknown',
                external_id=data.get('external_id'),
            )
        except serializers.ValidationError as e:
            form.add_error(None, str(e))
            return self.form_invalid(form)
        return HttpResponseRedirect(reverse('admin:manager_transaction_change', args=(transaction.transaction_id,)))

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = 'Remote Start Transaction'
        return data
