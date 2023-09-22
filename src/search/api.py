from django.db.models import Q
from django.http import JsonResponse

from rest_framework.decorators import api_view

from account.models import User
from account.serializers import UserSerializer
from post.models import Post
from post.serializers import PostSerializer
from page.models import Page
from page.serializers import PageSerializer
from marketplace.models import Product
from marketplace.serializers import ProductSerializer


@api_view(['POST'])
def search(request):
    data = request.data
    query = data['query']
    user_ids = [request.user.id]

    for user in request.user.friends.all():
        user_ids.append(user.id)

    users = User.objects.filter(Q(firstname__icontains=query) | Q(lastname__icontains=query))
    users_serializer = UserSerializer(users, many=True)

    posts = Post.objects.filter(
        Q(body__icontains=query) | 
        Q(created_by_id__in=list(user_ids), body__icontains=query) |
        Q(created_by__firstname__icontains=query) |
        Q(created_by__lastname__icontains=query)
    )

    posts_serializer = PostSerializer(posts, many=True)
    
    pages = Page.objects.filter(
        Q(name__icontains=query) | 
        Q(created_by_id__in=list(user_ids), name__icontains=query) |
        Q(created_by__firstname__icontains=query) |
        Q(created_by__lastname__icontains=query)
    )

    pages_serializer = PageSerializer(pages, many=True)

    products = Product.objects.filter(
        Q(name__icontains=query) | 
        Q(created_by_id__in=list(user_ids), name__icontains=query) |
        Q(created_by__firstname__icontains=query) |
        Q(created_by__lastname__icontains=query)
    )

    products_serializer = ProductSerializer(products, many=True)

    
    return JsonResponse({
        'users': users_serializer.data,
        'posts': posts_serializer.data,
        'pages': pages_serializer.data,
        'products': products_serializer.data,
    }, safe=False)