from rest_framework import serializers

from .models import Item, Farm


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'category', 'farm', 'price', 'quantity', 'description', 'image', 'unit']


class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = ['id', 'farm_name', 'address', 'inventory']
