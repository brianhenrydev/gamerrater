from django.shortcuts import get_object_or_404
from gamerraterapi.models import Game, GameImage
from gamerraterapi.views.game import GameSerializer
from gamerraterapi.views.user import UserSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
import uuid
import base64
import logging


class GameImageSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)

    game = GameSerializer(read_only=True)

    def get_is_owner(self, obj):
        return self.context["request"].user == obj.user

    class Meta:
        model = GameImage
        fields = [
            "id",
            "game",
            "user",
            "image",
            "created_at",
            "is_owner",
        ]


class GameImageViewSet(viewsets.ModelViewSet):
    def list(self, request):
        game_images = GameImage.objects.all()
        serializer = GameImageSerializer(
            game_images,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        print("test")
        game_id = request.data.get("game")
        game = get_object_or_404(Game, id=game_id)
        print(f"game: {game}, type(game): {type(game)}")
        print(f"user: {request.user}, type(request.user): {type(request.user)}")

        format, imgstr = request.data["image"].split(";base64,")
        ext = format.split("/")[-1]
        data = ContentFile(
            base64.b64decode(imgstr),
            name=f"{request.data['game']}-{uuid.uuid4()}.{ext}",
        )
        print("Error in GameImageViewSet:")
        print(f"data: {data}, type(data): {type(data)}")

        if not data:
            return Response(
                {"error": "Image and game are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        game = GameImage.objects.create(image=data, user=request.user, game=game)

        serialized = GameImageSerializer(game, context={"request": request})
        return Response(serialized.data, status=status.HTTP_201_CREATED)
