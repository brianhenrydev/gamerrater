from django.contrib import auth
from gamerraterapi.models.category import Category
from gamerraterapi.models.game import Game
from gamerraterapi.models.game_category import GameCategory
from gamerraterapi.views.user import UserSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from django.db.models import Q
import logging

from django.core.files.base import ContentFile
import uuid
import base64

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


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

    average_rating = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        return self.context["request"].user == obj.user

    def get_average_rating(self, obj):
        return obj.average_rating

    class Meta:
        model = Game
        fields = [
            "id",
            "title",
            "user",
            "average_rating",
            "is_owner",
            "description",
            "image",
            "designer",
            "categories",
            "release_year",
            "time_to_complete_estimate",
            "recommended_age",
            "created_at",
        ]


class GameViewSet(viewsets.ViewSet):
    def list(self, request):
        search_text = request.query_params.get("q", "")
        order_by = request.query_params.get("orderby", "")
        try:
            if search_text:
                games = Game.objects.filter(
                    Q(title__icontains=search_text)
                    | Q(description__icontains=search_text)
                    | Q(designer__icontains=search_text)
                )
            elif order_by:
                try:
                    games = Game.objects.order_by(order_by)

                except Exception as ex:
                    logging.error("Error in GameViewSet.list (order_by): %s", ex)
                    return Response(
                        {"details": f"no {order_by} porperty on this resource"},
                        status=status.HTTP_404_NOT_FOUND,
                    )

            else:
                games = Game.objects.all()

            serializer = GameSerializer(games, many=True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            logging.error("Error in GameViewSet.list: %s", ex)
            return Response(None, status=status.HTTP_404_NOT_FOUND)

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
        designer = request.data.get("designer")
        categories = request.data.get("categories", [])

        # Handle optional base64-encoded image
        image = None
        if "image" in request.data and request.data["image"]:
            format, imgstr = request.data["image"].split(";base64,")
            ext = format.split("/")[-1]
            image = ContentFile(
                base64.b64decode(imgstr),
                name=f"{request.data['title']}-{uuid.uuid4()}.{ext}",
            )

        game = Game.objects.create(
            title=title,
            description=description,
            user=user,
            image=image,
            designer=designer,
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

    def update(self, request, pk=None):
        try:
            game = Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

        if request.user != game.user:
            return Response(
                {"detail": "You do not have permission to edit this game."},
                status=status.HTTP_403_FORBIDDEN,
            )

        game.title = request.data.get("title", game.title)
        game.description = request.data.get("description", game.description)
        game.designer = request.data.get("designer", game.designer)
        game.release_year = request.data.get("release_year", game.release_year)
        game.time_to_complete_estimate = request.data.get(
            "time_to_complete_estimate", game.time_to_complete_estimate
        )
        game.recommended_age = request.data.get("recommended_age", game.recommended_age)

        # Handle optional base64-encoded image
        if "image" in request.data and request.data["image"]:
            format, imgstr = request.data["image"].split(";base64,")
            ext = format.split("/")[-1]
            game.image = ContentFile(
                base64.b64decode(imgstr),
                name=f"{request.data['title']}-{uuid.uuid4()}.{ext}",
            )
        else:
            game.image = None

        game.save()

        categories = request.data.get("categories", [])
        game.gamecategory_set.all().delete()  # Clear existing categories
        for category_id in categories:
            GameCategory.objects.create(
                game=game,
                category_id=category_id,
                user=request.user,
            )

        serialized = GameSerializer(game, context={"request": request})
        return Response(serialized.data, status=status.HTTP_200_OK)
