from django.contrib import auth
from gamerraterapi.models.game import Game
from gamerraterapi.models.game_rating import GameRating
from gamerraterapi.views.user import UserSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameRating
        fields = ["id", "user", "game", "rating"]


class RatingViewSet(viewsets.ViewSet):
    def list(self, request):
        ratings = GameRating.objects.all()
        serializer = RatingSerializer(ratings, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            rating = GameRating.objects.get(pk=pk)
            serializer = RatingSerializer(rating, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except GameRating.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        rating = request.data.get("rating")
        user = request.user
        game_id = request.data.get("game")

        try:
            game = Game.objects.get(pk=game_id)
        except Game.DoesNotExist:
            Response({"detail": "Game not found"}, status=status.HTTP_404_NOT_FOUND)

        existing_rating = GameRating.objects.filter(user=user, game=game).first()
        if existing_rating:
            existing_rating.rating = rating
            existing_rating.save()

            serialized = RatingSerializer(existing_rating, context={"request": request})
            return Response(serialized.data, status=status.HTTP_200_OK)
        else:
            rating = GameRating.objects.create(game=game, user=user, rating=rating)
            serialized = RatingSerializer(rating, context={"request": request})
            return Response(serialized.data, status=status.HTTP_201_CREATED)
