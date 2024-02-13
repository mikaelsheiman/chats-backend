from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from .serializers import *
from .models import Chat
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from minio import Minio

minio_client = Minio(endpoint="localhost:9000",
                     access_key="minioadmin",
                     secret_key="minioadmin",
                     secure=False)


@api_view(['GET'])
def get_chats(request):
    search_filter = request.GET.get('filter')
    
    if search_filter is not None:
        chats = Chat.active_objects.filter(name__contains=search_filter)
    else:
        chats = Chat.active_objects.all()

    serializer = ChatSerializer(chats, many=True)

    return Response({'data': serializer.data, 'filter': search_filter})


@api_view(['POST'])
def create_chat(request):
    serializer = ChatSerializer(data=request.data)

    if serializer.is_valid():
        serializer.validated_data
        serializer.save(admin=request.user.client)

        return Response(serializer.data, status=status.HTTP_201_CREATED) # redirect to chat/<id>
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_chat(request, id):
    client = request.user.client
    chat = Chat.active_objects.get(pk=id)
    chat_client = None

    try:
        chat_client = ChatClients.objects.get(chat=chat, client=client)
    except ChatClients.DoesNotExist as exept:
        return Response({'error': type(exept).__name__}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    serializer = ChatSerializer(chat)
    cc_serializer = ChatClientsSerializer(chat_client)

    return Response({'chat_data': serializer.data, 'client_data': cc_serializer.data})

@api_view(['DELETE'])
def delete_chat(request, id):
    chat = Chat.active_objects.get(pk=id)
    chat.logic_delete()

# /chats/
class ChatList(APIView):
    model_class = Chat
    serializer_class = ChatListSerializer
    
    def get(self, request, format=None):
        search_filter = request.GET.get('filter')
        chats = self.model_class.active_objects.all()
        if search_filter is not None:
            chats = self.model_class.active_objects.filter(name__contains=search_filter)
        serializer = self.serializer_class(chats, many=True)

        return Response({'data': serializer.data, 'filter': search_filter})
    
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.validated_data
            serializer.save(admin=request.user.client)

            return Response(serializer.data, status=status.HTTP_201_CREATED) # redirect to chat/<id>
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# /chat/<int:id>/
class ChatDetails(APIView):
    model_class = Chat
    serializer_class = ChatSerializer

    def get(self, request, id, format=None):
        client = request.user.client
        chat = Chat.active_objects.get(pk=id)
        chat_client = None

        try:
            chat_client = ChatClients.objects.get(chat=chat, client=client)
        except ChatClients.DoesNotExist as exept:
            return Response({'error': type(exept).__name__}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        serializer = self.serializer_class(chat)
        cc_serializer = ChatClientsSerializer(chat_client)

        return Response({'chat_data': serializer.data, 'client_data': cc_serializer.data})
    
    def delete(self, request, id):
        chat = Chat.active_objects.get(pk=id)
        chat.logic_delete()


# /chat/<int:id>/message
class MessageHandler(APIView):
    model_class = Message
    serializer_class = MessageSerializer

    def post(self, request, id):
        serializer = self.serializer_class(data=request.data)
        serializer.initial_data["image"] = request.FILES['image']
        if serializer.is_valid():
            serializer.validated_data['client'] = request.user.client
            serializer.validated_data['chat'] = Chat.objects.get(pk=id)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) # redirect to chat/<id>
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.update(request.user.client)
            return Response(serializer.data, status=status.HTTP_201_CREATED) # redirect to chat/<id>
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['POST'])
def post_message(request, id):
    serializer = MessageSerializer(data=request.data)
    serializer.initial_data["image"] = request.FILES['image']
    if serializer.is_valid():
        serializer.validated_data['client'] = request.user.client
        serializer.validated_data['chat'] = Chat.objects.get(pk=id)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED) # redirect to chat/<id>
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)