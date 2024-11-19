from django.urls import path
from .views import ProductListView, InventoryManagementView, LowStockNotificationView, ProductDetailView, \
    ProductListViewForBuyer

urlpatterns = [
    path('farmer/', ProductListView.as_view(), name='product-list'),  # GET /api/products/
    path('<int:pk>/inventory/', InventoryManagementView.as_view(), name='inventory-management'), # PUT /api/products/<id>/inventory/
    path('low-stock/', LowStockNotificationView.as_view(), name='low-stock-notifications'),
    path('buyer/', ProductListViewForBuyer.as_view(), name='product-list'),
    path('buyer/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    # GET /api/products/low-stock/
]
