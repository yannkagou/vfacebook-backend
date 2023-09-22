from django.urls import path

from . import api


urlpatterns = [
    path('', api.post_list, name='post_list'),
    path('<int:id>/', api.post_detail, name='post_detail'),
    path('<int:id>/like/', api.post_like, name='post_like'),
    path('<int:id>/delete/', api.post_delete, name='post_delete'),
    path('<int:id>/comment/', api.post_create_comment, name='post_create_comment'),
    path('profile/<int:id>/', api.post_list_profile, name='post_list_profile'),
    path('create/', api.post_create, name='post_create'),
    path('story/', api.story_list, name='story_list'),
    path('story/create/', api.story_create, name='story_create'),
    path('story/<int:id>/', api.story_detail, name='story_detail'),
    path('story/<int:id>/delete/', api.story_delete, name='story_delete'),
    path('trends/', api.get_trends, name='trends'),
]