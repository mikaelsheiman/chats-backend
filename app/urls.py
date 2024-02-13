from django.urls import path
from .views import *

urlpatterns = [
    # Набор методов для услуг
    path('api/chats/search/', search_chats),  # GET
    path('api/chats/<int:chat_id>/', get_chat_by_id),  # GET
    path('api/chats/<int:chat_id>/image/', get_chat_image),  # GET
    path('api/chats/<int:chat_id>/update/', update_chat),  # PUT
    path('api/chats/<int:chat_id>/update_image/', update_chat_image),  # PUT
    path('api/chats/<int:chat_id>/delete/', delete_chat),  # DELETE
    path('api/chats/create/', create_chat),  # POST
    path('api/chats/<int:chat_id>/add_to_message/', add_chat_to_message),  # POST

    # Набор методов для заявок
    path('api/messages/search/', search_messages),  # GET
    path('api/messages/<int:message_id>/', get_message_by_id),  # GET
    path('api/messages/<int:message_id>/update/', update_message),  # PUT
    path('api/messages/<int:message_id>/update_check_spam/', update_message_check_spam),  # PUT
    path('api/messages/<int:message_id>/update_status_user/', update_status_user),  # PUT
    path('api/messages/<int:message_id>/update_status_admin/', update_status_admin),  # PUT
    path('api/messages/<int:message_id>/delete/', delete_message),  # DELETE
    path('api/messages/<int:message_id>/delete_chat/<int:chat_id>/', delete_chat_from_message),  # DELETE
 
    # Набор методов для аутентификации и авторизации
    path("api/register/", register),
    path("api/login/", login),
    path("api/check/", check),
    path("api/logout/", logout)
]
