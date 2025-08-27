from django.urls import path
from .views import  OrderDetailView, OrderUpdateView, OrderCreateView, ProductListCreateView, ClientListCreateView

urlpatterns = [
    path('clients/', ClientListCreateView.as_view(), name='client-list-create'),

    path('products/', ProductListCreateView.as_view(), name='product-list-create'),

    path('orders/', OrderCreateView.as_view(), name='order-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:pk>/update/', OrderUpdateView.as_view(), name='order-update'),
]