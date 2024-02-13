from django.shortcuts import render
from django.http import HttpResponse
from datetime import date

local_data = {
    'chat_list': [
        {
            'chat_id' : 0,
            'chat_image' : 'dialog-svgrepo-com.svg',
            'chat_name' : 'Название чата 0',
            'last_message_time' : '12:34',
            'last_message' : 'Последнее сообщение в чате',
            'unread_messages' : 5,
            'members_count' : 2,
        },
        {
            'chat_id' : 1,
            'chat_image' : 'dialog-svgrepo-com.svg',
            'chat_name' : 'Название чата 1',
            'last_message_time' : '12:35',
            'last_message' : 'Последнее сообщение в чате 2 ооолоолоололололол',
            'unread_messages' : 62,
            'members_count' : 3,
        },
        {
            'chat_id' : 2,
            'chat_image' : 'dialog-svgrepo-com.svg',
            'chat_name' : 'Название чата 2',
            'last_message_time' : '12:35',
            'last_message' : 'Последнее сообщение в чате 2',
            'unread_messages' : 623,
            'members_count' : 4,
        },
        {
            'chat_id' : 3,
            'chat_image' : 'dialog-svgrepo-com.svg',
            'chat_name' : 'Название чата 3',
            'last_message_time' : '12:35',
            'last_message' : 'Последнее сообщение в чате 2',
            'unread_messages' : 6234,
            'members_count' : 5,
        },
    ],
    'message_list' : [
        {
            'chat_id' : 0,
            'author' : 'John Smith',
            'text' : 'Hi! My name is John Smith 0!',
            'time' : '12:00',
        },
        {
            'chat_id' : 0,
            'author' : 'John Smith',
            'text' : 'Hi! My name is John Smith 1! this message is longer',
            'time' : '12:01',
        },
        {
            'chat_id' : 0,
            'author' : 'John Smith',
            'text' : 'Hi! My name is John Smith 2! this message is far longer then the previous one',
            'time' : '12:02',
        },
        {
            'chat_id' : 0,
            'author' : 'John Smith',
            'text' : 'Hi! My name is John Smith 2! this message is far longer then the previous one',
            'time' : '12:02',
        },
        {
            'chat_id' : 0,
            'author' : 'John Smith',
            'text' : 'Hi! My name is John Smith 2! this message is far longer then the previous one',
            'time' : '12:02',
        },
        {
            'chat_id' : 0,
            'author' : 'John Smith',
            'text' : 'Hi! My name is John Smith 2! this message is far longer then the previous one',
            'time' : '12:02',
        },
        {
            'chat_id' : 1,
            'author' : 'John Smith',
            'text' : 'Hi! My name is John Smith 2! this message is far longer then the previous one',
            'time' : '12:02',
        },
        {
            'chat_id' : 1,
            'author' : 'John Smith',
            'text' : 'Hi! My name is John Smith 2! this message is far longer then the previous one',
            'time' : '12:02',
        },
        {
            'chat_id' : 1,
            'author' : 'You',
            'text' : 'я нипонимаю по англиски',
            'time' : '12:20',
        },
    ],
}


def GetChats(request):
    if request.method == 'POST':
        search_filter = request.POST['text']
        return render(request, 'main.html', { 'data' : {
            'search_filter' : search_filter,
            'chat_list' : filter(lambda x: (search_filter in x['chat_name']), local_data['chat_list'])
        }})

    return render(request, 'main.html', { 'data' : {
        'chat_list' : local_data['chat_list']
    }})



def GetChat(request, id):

    if request.method == 'POST':
        search_filter = request.POST['text']
        return render(request, 'chat_entity.html', { 'data' : {
            'search_filter' : search_filter,
            'chat' : local_data['chat_list'][id],
            'messages' : filter(lambda x: (x['chat_id'] == id and search_filter in x['text']), local_data['message_list']),
        }})
    
    return render(request, 'chat_entity.html', { 'data' : {
        # 'search_filter' : search_filter,
        'chat' : local_data['chat_list'][id],
        'messages' : filter(lambda x: (x['chat_id'] == id), local_data['message_list']),
    }})
