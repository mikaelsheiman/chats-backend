import requests
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.utils.dateparse import parse_datetime
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .jwt_helper import *
from .permissions import *
from .serializers import *
from .utils import identity_user


def get_draft_message(request):
    user = identity_user(request)

    if user is None:
        return None

    message = Message.objects.filter(owner_id=user.id).filter(status=1).first()

    return message


@api_view(["GET"])
def search_chats(request):
    query = request.GET.get("query", "")

    chat = Chat.objects.filter(status=1).filter(name__icontains=query)

    serializer = ChatSerializer(chat, many=True)

    draft_message = get_draft_message(request)

    resp = {
        "chats": serializer.data,
        "draft_message_id": draft_message.pk if draft_message else None
    }

    return Response(resp)


@api_view(["GET"])
def get_chat_by_id(request, chat_id):
    if not Chat.objects.filter(pk=chat_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    chat = Chat.objects.get(pk=chat_id)
    serializer = ChatSerializer(chat)

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_chat(request, chat_id):
    if not Chat.objects.filter(pk=chat_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    chat = Chat.objects.get(pk=chat_id)
    serializer = ChatSerializer(chat, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsModerator])
def create_chat(request):
    chat = Chat.objects.create()

    serializer = ChatSerializer(chat)

    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_chat(request, chat_id):
    if not Chat.objects.filter(pk=chat_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    chat = Chat.objects.get(pk=chat_id)
    chat.status = 2
    chat.save()

    chat = Chat.objects.filter(status=1)
    serializer = ChatSerializer(chat, many=True)

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_chat_to_message(request, chat_id):
    if not Chat.objects.filter(pk=chat_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    chat = Chat.objects.get(pk=chat_id)

    message = get_draft_message(request)

    if message is None:
        message = Message.objects.create()
        message.date_perform = timezone.now()

    if message.chats.contains(chat):
        return Response(status=status.HTTP_409_CONFLICT)

    message.chats.add(chat)
    message.owner = identity_user(request)
    message.save()

    serializer = MessageSerializer(message)
    return Response(serializer.data)


@api_view(["GET"])
def get_chat_image(request, chat_id):
    if not Chat.objects.filter(pk=chat_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    chat = Chat.objects.get(pk=chat_id)

    return HttpResponse(chat.image, content_type="image/png")


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_chat_image(request, chat_id):
    if not Chat.objects.filter(pk=chat_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    chat = Chat.objects.get(pk=chat_id)
    serializer = ChatSerializer(chat, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_messages(request):
    user = identity_user(request)

    status_id = int(request.GET.get("status", -1))
    date_start = request.GET.get("date_start")
    date_end = request.GET.get("date_end")

    messages = Message.objects.exclude(status__in=[1, 5])

    if not user.is_moderator:
        messages = messages.filter(owner=user)

    if status_id > 0:
        messages = messages.filter(status=status_id)

    if date_start and parse_datetime(date_start):
        messages = messages.filter(date_formation__gte=parse_datetime(date_start))

    if date_end and parse_datetime(date_end):
        messages = messages.filter(date_formation__lte=parse_datetime(date_end))

    serializer = MessagesSerializer(messages, many=True)

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_message_by_id(request, message_id):
    if not Message.objects.filter(pk=message_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    message = Message.objects.get(pk=message_id)
    serializer = MessageSerializer(message)

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_message(request, message_id):
    if not Message.objects.filter(pk=message_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    message = Message.objects.get(pk=message_id)

    serializer = MessageSerializer(message, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    message.save()

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsRemoteService])
def update_message_check_spam(request, message_id):
    if not Message.objects.filter(pk=message_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    message = Message.objects.get(pk=message_id)

    serializer = MessageSerializer(message, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    message.save()

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_status_user(request, message_id):
    if not Message.objects.filter(pk=message_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    message = Message.objects.get(pk=message_id)

    message.status = 2
    message.date_formation = timezone.now()
    message.save()

    calculate_check_spam(message_id)
    
    serializer = MessageSerializer(message)

    return Response(serializer.data)


def calculate_check_spam(message_id):
    data = {
        "message_id": message_id
    }

    requests.post("http://127.0.0.1:8080/check_spam/", json=data, timeout=3)

@api_view(["PUT"])
@permission_classes([IsModerator])
def update_status_admin(request, message_id):
    if not Message.objects.filter(pk=message_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_status = int(request.data["status"])

    if request_status not in [3, 4]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    message = Message.objects.get(pk=message_id)

    if message.status != 2:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    message.moderator = identity_user(request)
    message.status = request_status
    message.date_complete = timezone.now()
    message.save()

    serializer = MessageSerializer(message)

    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_message(request, message_id):
    if not Message.objects.filter(pk=message_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    message = Message.objects.get(pk=message_id)

    if message.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    message.status = 5
    message.save()

    return Response(status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_chat_from_message(request, message_id, chat_id):
    if not Message.objects.filter(pk=message_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not Chat.objects.filter(pk=chat_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    message = Message.objects.get(pk=message_id)
    message.chats.remove(Chat.objects.get(pk=chat_id))
    message.save()

    if message.chats.count() == 0:
        message.delete()
        return Response(status=status.HTTP_201_CREATED)

    return Response(status=status.HTTP_200_OK)


@swagger_auto_schema(method='post', request_body=UserLoginSerializer)
@api_view(["POST"])
def login(request):
    serializer = UserLoginSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    user = authenticate(**serializer.data)
    if user is None:
        message = {"message": "invalid credentials"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    access_token = create_access_token(user.id)

    user_data = {
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
        "is_moderator": user.is_moderator,
        "access_token": access_token
    }

    return Response(user_data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def register(request):
    serializer = UserRegisterSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(status=status.HTTP_409_CONFLICT)

    user = serializer.save()

    access_token = create_access_token(user.id)

    message = {
        'message': 'User registered successfully',
        'user_id': user.id,
        "access_token": access_token
    }

    return Response(message, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def check(request):
    token = get_access_token(request)

    if token is None:
        message = {"message": "Token is not found"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    if token in cache:
        message = {"message": "Token in blacklist"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    payload = get_jwt_payload(token)
    user_id = payload["user_id"]

    user = CustomUser.objects.get(pk=user_id)
    serializer = UserSerializer(user)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    access_token = get_access_token(request)

    if access_token not in cache:
        cache.set(access_token, settings.JWT["ACCESS_TOKEN_LIFETIME"])

    message = {
        "message": "Вы успешно вышли из аккаунта"
    }

    return Response(message, status=status.HTTP_200_OK)
