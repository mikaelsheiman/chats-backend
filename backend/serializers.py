from .models import *
from rest_framework import serializers

class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ["id", "first_name", "last_name", "nickname"]


class MessageSerializer(serializers.ModelSerializer):

    chats = serializers.PrimaryKeyRelatedField(many=True, queryset=Chat.active_objects.all())
    client = ClientSerializer(read_only = True)
    image = serializers.ImageField()

    class Meta:
        model = Message
        fields = ["chats", "client", "text", "datetime", "image"]

class ChatListSerializer(serializers.ModelSerializer):

    clients = serializers.PrimaryKeyRelatedField(many=True, queryset=Client.active_objects.all(),)
    
    def create(self, validated_data):
        admin = validated_data.pop('admin')
        clients = validated_data.pop('clients')
        # image = validated_data.pop('image')
        chat = Chat.objects.create(**validated_data)
        chat.clients.set(clients)
        if(admin):
            ChatClients.objects.get(chat=chat, client=admin).set_admin()
        return chat

    class Meta:
        model = Chat
        fields = ["name", "image_path", "messages_total", "last_update_time", "clients",]

class ChatSerializer(serializers.ModelSerializer):

    clients = serializers.PrimaryKeyRelatedField(many=True, queryset=Client.active_objects.all(),)
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Chat
        fields = ["name", "image", "messages_total", "last_update_time", "clients", "messages"]


class ChatClientsSerializer(serializers.ModelSerializer):

    unread_messages = serializers.IntegerField(read_only=True)

    class Meta:
        model = ChatClients
        fields = ['is_admin', 'unread_messages']


