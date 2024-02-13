"""
URL configuration for carriegram project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from backend import views
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path(r'chats/search', views.get_chats, name='get_chats'),
    path(r'chats/create', views.create_chat, name='post_chat'),
    path(r'chat/<int:id>/', views.get_chat, name='get_chat'),
    path(r'chat/<int:id>/message', views.MessageHandler.as_view(), name='message'),
    #path(r'backend/<int:pk>/put/', views.put_detail, name='stocks-put'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]

# urlpatterns2 = [
#     path('admin/', admin.site.urls),
#     path('chats/', views.GetChats, name='chats'),
#     path('chat/<int:id>/', views.GetChat, name='chat_url'),
#     path('chat/<int:id>/filter', views.GetChat, name='filter'),
#     path('chat/<int:id>/delete', views.DeleteChat, name='delete_chat'),
#     path('chats/new_chat', views.CreateChat, name='new_chat'),
#     path('login/', views.login_user, name='login'),
#     path('chats/logout/', views.logout_user, name='logout'),
# ]