from django.urls import path

from manager import views

app_name = 'manager'

urlpatterns = [
    path(
        'transactions/remote-start-transaction/',
        views.RemoteStartTransactionView.as_view(),
        name='remote-start-transaction',
    ),
    path(
        'transactions/remote-stop-transaction/',
        views.RemoteStopTransactionView.as_view(),
        name='remote-stop-transaction',
    )
]
