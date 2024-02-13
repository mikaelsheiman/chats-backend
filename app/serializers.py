from rest_framework import serializers

from .models import *


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    chats = ChatSerializer(read_only=True, many=True)
    owner = serializers.SerializerMethodField()
    moderator = serializers.SerializerMethodField()

    def get_owner(selfself, order):
        return order.owner.name

    def get_moderator(selfself, order):
        if order.moderator:
            return order.moderator.name

        return ""

    class Meta:
        model = Message
        fields = "__all__"


class MessagesSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    moderator = serializers.SerializerMethodField()

    def get_owner(selfself, order):
        return order.owner.name

    def get_moderator(selfself, order):
        if order.moderator:
            return order.moderator.name

        return ""

    class Meta:
        model = Message
        fields = "__all__"
        
        
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password', 'name')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data['email'],
            name=validated_data['name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)