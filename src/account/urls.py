from django.urls import path
from . import api

urlpatterns = [
    path('signup/', api.signup_view, name='signup_view'),
    path('login/', api.login_view, name='login_view'),
    path('logout/', api.logout_view, name='logout_view'),
    path('user/', api.user_detail, name='user_detail'),
    path('editprofile/', api.editprofile, name='editprofile'),
    path('friends/<int:id>/', api.friends, name='friends'),
    path('friends/<int:id>/unfollow/', api.unfollow, name='unfollow'),
    path('friends/<int:id>/request/', api.send_friendship_request, name='send_friendship_request'),
    path('friends/<int:id>/<str:status>/', api.handle_request, name='handle_request'),
]