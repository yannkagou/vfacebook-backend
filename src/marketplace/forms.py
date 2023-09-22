from django.forms import ModelForm, forms

from .models import Category, Product


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'image', 'location')
        