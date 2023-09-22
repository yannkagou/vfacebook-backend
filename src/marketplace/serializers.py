from rest_framework.serializers import ModelSerializer

from .models import Category, Product
from account.serializers import UserSerializer
        
class CategorySerializer(ModelSerializer):
    # products = ProductSerializer(read_only=True, many=True)
    class Meta:
        model = Category
        fields = ('id', 'name',)
        
class ProductSerializer(ModelSerializer):
    created_by = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'created_at', 'location', 'get_image', 'price', 'created_by', 'category',)
