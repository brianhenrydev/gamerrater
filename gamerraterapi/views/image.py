from django.contrib import auth
from django.shortcuts import get_object_or_404
from gamerraterapi.models import Game, GameImage
from gamerraterapi.views.game import GameSerializer
from gamerraterapi.views.user import UserSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth.models import User


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
    parser_classes = [MultiPartParser, FormParser]

    def list(self, request):
        game_images = GameImage.objects.all()
        serializer = GameImageSerializer(
            game_images,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        image = request.FILES.get("image")

        game_id = request.data.get("game")

        user = User.objects.get(pk=request.user.id)
        game = get_object_or_404(Game, id=game_id)

        if not image:
            return Response(
                {"error": "Image and game are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        game = GameImage.objects.create(image=image, user=user, game=game)

        serialized = GameImageSerializer(game, context={"request": request})
        return Response(serialized.data, status=status.HTTP_201_CREATED)
