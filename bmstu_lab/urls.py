"""
URL configuration for bmstu_lab project.

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
from django.urls import path
from lab import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chats/', views.GetChats, name='chats'),
    path('chats/filter', views.GetChats, name='chats_filter'),
    path('chat/<int:id>/', views.GetChat, name='chat_url'),
    path('chat/<int:id>/filter', views.GetChat, name='filter'),
    path('chat/<int:id>/send', views.SendMessage, name='send'),
    path('chat/<int:id>/delete', views.DeleteChat, name='delete_chat'),
    path('chats/new_chat', views.CreateChat, name='new_chat'),
    path('chats/new_multimessage', views.SendMultiMessage, name="new_multimessage"),
    path('login/', views.login_user, name='login'),
    path('chats/logout/', views.logout_user, name='logout'),
]
