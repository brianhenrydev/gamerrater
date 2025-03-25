from django.contrib import auth
from gamerraterapi.models.category import Category
from gamerraterapi.models.game import Game
from gamerraterapi.models.game_category import GameCategory
from gamerraterapi.views.user import UserSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers


class GameCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GameCategory
        fields = []


class GameSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()
    categories = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all(), source="gamecategory_set"
    )

    user = UserSerializer(read_only=True)

    def get_is_owner(self, obj):
        return self.context["request"].user == obj.user

    class Meta:
        model = Game
        fields = [
            "id",
            "title",
            "user",
            "average_rating",
            "is_owner",
            "description",
            "categories",
            "release_year",
            "time_to_complete_estimate",
            "recommended_age",
        ]


class GameViewSet(viewsets.ViewSet):
    def list(self, request):
        games = Game.objects.all()
        serializer = GameSerializer(
            games,
            many=True,
            context={"request": request},  # Allow serializer to access request
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            game = Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

        serializer = GameSerializer(game, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        title = request.data.get("title")
        description = request.data.get("description")
        user = request.user
        release_year = request.data.get("release_year")
        time_to_complete_estimate = request.data.get("time_to_complete_estimate")
        recommended_age = request.data.get("recommended_age")
        categories = request.data.get("categories", [])

        game = Game.objects.create(
            title=title,
            description=description,
            user=user,
            release_year=release_year,
            time_to_complete_estimate=time_to_complete_estimate,
            recommended_age=recommended_age,
        )

        for category_id in categories:
            GameCategory.objects.create(
                game=game,
                category_id=category_id,
                user=request.user,
            )

        serialized = GameSerializer(game, context={"request": request})
        return Response(serialized.data, status=status.HTTP_201_CREATED)
