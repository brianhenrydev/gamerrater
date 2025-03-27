from gamerraterapi.models.game import Game
from gamerraterapi.models.game_review import GameReview
from gamerraterapi.views.user import UserSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
import logging
from django.db.models import Q


class GameCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GameReview
        fields = []


class GameReviewSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()

    user = UserSerializer(read_only=True)

    def get_is_owner(self, obj):
        return self.context["request"].user == obj.user

    class Meta:
        model = GameReview
        fields = ["id", "user", "game", "is_owner", "content", "created_at"]


class GameReviewViewSet(viewsets.ViewSet):
    def list(self, request):
        game_id = request.query_params.get("game_id", None)
        search_text = request.query_params.get("q", "")
        order_by = request.query_params.get("orderby", "")
        try:
            if game_id is not None:
                reviews = GameReview.objects.filter(game_id=game_id)

            elif search_text:
                reviews = GameReview.objects.filter(Q(content__icontains=search_text))
            elif order_by:
                try:
                    reviews = GameReview.objects.order_by(order_by)

                except Exception as ex:
                    logging.error("Error in GameViewSet.list (order_by): %s", ex)
                    return Response(
                        {"details": f"no {order_by} porperty on this resource"},
                        status=status.HTTP_404_NOT_FOUND,
                    )

            else:
                reviews = GameReview.objects.all()

            serializer = GameReviewSerializer(
                reviews, many=True, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            logging.error("Error in GameViewSet.list: %s", ex)
            return Response(None, status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, pk=None):
        try:
            review = GameReview.objects.get(pk=pk)
        except GameReview.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

        serializer = GameReviewSerializer(
            review,
            many=False,
            context={"request": request},
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        user = request.user
        game_id = request.data.get("game")
        game = Game.objects.get(pk=game_id)
        content = request.data.get("content")

        review = GameReview.objects.create(game=game, user=user, content=content)

        serialized = GameReviewSerializer(review, context={"request": request})
        return Response(serialized.data, status=status.HTTP_201_CREATED)
