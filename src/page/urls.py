from django.urls import path

from . import api


urlpatterns = [
    path('', api.page_list, name='page_list'),
    path('create/', api.page_create, name='page_create'),
    path('<int:page_id>/', api.page_detail, name='page_detail'),
    path('<int:page_id>/delete/', api.page_delete, name='page_delete'),
    path('profile/<int:id>/', api.page_list_profile, name='page_list_profile'),
    path('<int:page_id>/subscribe/', api.subscribe_page, name='page_subscription'),
    path('<int:page_id>/<int:id>/admin', api.page_add_admins, name='page_add_admin'),
    path('<int:page_id>/createpost/', api.page_post_create, name='page_create_post'),
    path('<int:page_id>/createstory/', api.page_story_create, name='page_create_story'),
    path('<int:page_id>/<int:post_id>/like/', api.page_post_like, name='page_post_like'),
    path('<int:page_id>/<int:post_id>/delete/', api.page_post_delete, name='page_post_delete'),
    path('<int:page_id>/<int:post_id>/comment/', api.page_post_create_comment, name='page_post_comment'),
]