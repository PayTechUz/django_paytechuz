from django.urls import path
from apps.shop.views import CreateOrderAPIView

app_name = 'shop'


urlpatterns = [
    path('api/orders/create', CreateOrderAPIView.as_view(), name='create_order'),
]
