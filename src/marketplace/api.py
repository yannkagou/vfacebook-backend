from marketplace.forms import ProductForm
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from django.http import JsonResponse
from rest_framework.decorators import api_view

from account.models import User


@api_view(['GET'])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    
    return JsonResponse(serializer.data, safe=False)


# @api_view(['GET'])
# def category_detail(request, id):
#     category = Category.objects.get(id=id)
#     serializer = CategorySerializer(category)
    
#     return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def product_profile(request, id):
    products = Product.objects.filter(created_by_id=id)
    products_serializer = ProductSerializer(products, many=True)
    
    return JsonResponse(products_serializer.data, safe=False)

@api_view(['GET'])
def product_list_category(request, name):   
    category = Category.objects.get(name=name)
    products = Product.objects.filter(category__name=name)

    products_serializer = ProductSerializer(products, many=True)
    category_serializer = CategorySerializer(category)

    return JsonResponse({
        'products': products_serializer.data,
        'category': category_serializer.data
    }, safe=False)

@api_view(['GET'])
def product_detail(request, id):
    product = Product.objects.get(id=id)
    serializer = ProductSerializer(product)
    
    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def add_product(request, name):
    category = Category.objects.get(name=name)
    
    form = ProductForm(request.POST, request.FILES)
    
    if form.is_valid():
        product = form.save(commit=False)
        product.created_by = request.user
        
        product.category = category

        product.save()

        serializer = ProductSerializer(product)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'Invalid form data for product', 'errors': form.errors})

    
@api_view(['PUT'])
def update_product(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'})

    form = ProductForm(request.POST, request.FILES, instance=product)
    if form.is_valid():
        updated_product = form.save(commit=False)
        updated_product.created_by = request.user
        updated_product.save()

        serializer = ProductSerializer(updated_product)
        return JsonResponse(serializer.data)
    else:
        return JsonResponse({'error': 'Invalid form data for product'})

@api_view(['DELETE'])
def delete_product(request, id):
    try:
        product = Product.objects.filter(created_by=request.user).get(id=id)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'})
    
    product.delete()
    
    return JsonResponse({'message': 'Product deleted'})

