from django.db import models

from account.models import User

class Category(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        ordering = ('name',)
    
    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='product_category', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='product',on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-created_at',)
    
    def __str__(self):
        return self.name
    
    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return '/media/profile.png'