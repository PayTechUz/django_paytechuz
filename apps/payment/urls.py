# urls.py
from django.urls import path

from apps.payment.views import PaymeWebhookView, ClickWebhookView, AtmosWebhookView


urlpatterns = [
    path('payments/payme/webhook/', PaymeWebhookView.as_view(), name='payme_webhook'),
    path('payments/click/webhook', ClickWebhookView.as_view(), name='click_webhook'),
    path('payments/atmos/webhook/', AtmosWebhookView.as_view(), name='atmos_webhook'),
]
