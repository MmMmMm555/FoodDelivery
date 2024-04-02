from django.urls import path

from apps.orders.api_endpoints.order.views import (OrderListCreateView, OrderRetrieveUpdateDestroyView)

urlpatterns = [
    path('order/', OrderListCreateView.as_view(), name='list_create'),
    path('order/<int:pk>', OrderRetrieveUpdateDestroyView.as_view(), name='retrieve_update_delete'),
]
