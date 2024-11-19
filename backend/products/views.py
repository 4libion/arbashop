from django.db.models import Q
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Item
from .serializers import ItemSerializer

class ProductListView(APIView):
    def get(self, request):
        farmer_id = request.query_params.get('farmer_id')
        if farmer_id:
            items = Item.objects.filter(farm__id=farmer_id)
        else:
            items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Inventory management endpoint
class InventoryManagementView(APIView):
    def put(self, request, pk):
        try:
            item = Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        quantity = request.data.get('quantity')
        if quantity is not None:
            item.quantity = quantity
            item.save()
            return Response({"message": "Inventory updated successfully"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)


# Low-stock notification endpoint
class LowStockNotificationView(APIView):
    def get(self, request):
        low_stock_items = Item.objects.filter(quantity__lte=5)  # Threshold for low stock
        serializer = ItemSerializer(low_stock_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductListViewForBuyer(ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Search by name, category, or farm location
        search_query = self.request.query_params.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(category__name__icontains=search_query) |
                Q(farm__location__icontains=search_query)
            )

        # Filter by price range
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__name__icontains=category)

        # Sort by price or quantity
        sort_by = self.request.query_params.get('sort', 'id')
        if sort_by in ['price', 'quantity', '-price', '-quantity']:
            queryset = queryset.order_by(sort_by)

        return queryset

class ProductDetailView(APIView):
    def get(self, request, pk):
        try:
            product = Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ItemSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)