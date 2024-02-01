from django.urls import path

from manager import views

app_name = 'manager'

urlpatterns = [
    path(
        'transactions/remote-start-transaction/',
        views.RemoteStartTransactionView.as_view(),
        name='remote-start-transaction',
    )
]
