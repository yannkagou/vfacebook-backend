from django.urls import path
from . import api

urlpatterns = [
    path('', api.category_list, name='category_list'),
    # path('<int:id>/', api.category_detail, name='category_detail'),
    path('category/<str:name>/', api.product_list_category, name='product_list_category'),
    path('products/', api.product_list, name='product_list'),
    path('products/profile/<int:id>/', api.product_profile, name='product_profile'),
    path('products/<int:id>/', api.product_detail, name='product_detail'),
    path('products/add/<str:name>', api.add_product, name='add_product'),
    path('products/<int:id>/update/', api.update_product, name='update_product'),
    path('products/<int:id>/delete/', api.delete_product, name='delete_product'),
]