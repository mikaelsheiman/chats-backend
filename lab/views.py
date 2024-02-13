from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import date
from .models import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User as AUser
from django.db.models import Max



def GetChats(request):
    client = request.user.client

    if request.method == 'POST':
        search_filter = request.POST['text']
        chat_list = Chat.active_objects.filter(users__id__exact=client.id, name__contains=search_filter).order_by('last_message_time')
        return render(request, 'main.html', { 'data' : {
            'search_filter' : search_filter,
            'user_list' : Client.objects.all(),
            'chat_info' : [{
                'chat': chat, 
                'client': ChatUser.objects.get(chat=chat, user=client),
                # 'last_message': Message.objects.filter(chat=chat).order_by('-time').first(),
                'last_message': Message.objects.filter(chat=chat).last(),
                } for chat in chat_list
                ]
        }})
    else:
        chat_list = Chat.active_objects.filter(users__id__exact=client.id).order_by('last_message_time')
        return render(request, 'main.html', { 'data' : {
            'user_list' : Client.objects.all(),
            'chat_info' : [{
                'chat': chat, 
                'client': ChatUser.objects.get(chat=chat, user=client),
                'last_message': Message.objects.filter(chat=chat).last(),
                } for chat in chat_list
                ]
    }})



def GetChat(request, id):
    client = request.user.client
    chat = Chat.objects.get(pk=id)
    chat_user = ChatUser.objects.get(chat=chat, user=client)

    chat_user.update_read_messages()

    if request.method == 'POST':
        search_filter = request.POST['text']
        return render(request, 'chat_entity.html', { 'data' : {
            'search_filter' : search_filter,
            'chat' : chat,
            'messages' : Message.objects.filter(chat__id__exact=id, text__contains=search_filter),
        }})
    else:
        return render(request, 'chat_entity.html', { 'data' : {
            # 'search_filter' : search_filter,
            'chat' : chat,
            'messages' : Message.objects.filter(chat__id__exact=id),
        }})



def SendMessage(request, id):

    new_message = Message.objects.create(
        chat=Chat.objects.get(pk=id),
        user=request.user.client,
        text=request.POST['text'],
    )
    new_message.save()

    return redirect(reverse('chat_url', args=(id,)))



def CreateChat(request):

    try:
        new_chat_name = request.POST.get('new_name')
        members_list = request.POST.getlist('choices')
        
        new_chat = Chat(name=new_chat_name)
        new_chat.save()

        for id in members_list:
            client = Client.objects.get(id=id)
            admin = True if client == request.user.client else False
            new_chat.users.add(client, through_defaults={'is_admin': admin})

    except Exception as error:
        new_chat.delete()
        raise error
        # return redirect('chats')


    return redirect(reverse('chat_url', args=(new_chat.id,)))



def DeleteChat(request, id):

    client = request.user.client
    chat = Chat.objects.get(pk=id)
    chat_user = ChatUser.objects.get(user=client, chat=chat)

    if(chat_user.is_admin):
        Chat.objects.get(pk=id).logic_delete()
        return redirect('chats')
    
    else:
        return redirect(reverse('chat_url', args=(id,)))



def login_user(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        auth_user = authenticate(request, username=username, password=password)

        if auth_user is not None:
            login(request, auth_user)
            return redirect('chats')
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')
    


def logout_user(request):
    logout(request)
    return redirect('login')