from rest_framework import serializers
from apps.product.models import Product

class ProductSerializer(serializers.ModelSerializer):
    entry_date = serializers.DateField(format='%Y-%m-%d', input_formats=['%Y-%m-%d'])
    
    class Meta:
        model = Product
        fields = ['product_name', 'selling_price', 'available_quantity', 'entry_date', 'brand']

