from django.urls import path
from . import api

urlpatterns = [
    path('', api.conversation_list, name='conversation_list'),
    path('<int:id>/', api.conversation_detail, name='conversation_detail'),
    path('<int:id>/send/', api.conversation_send_message, name='conversation_send_message'),
    path('<int:user_id>/get-or-create/', api.conversation_get_or_create, name='conversation_get_or_create'),
]