from os.path import basename
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import include, path
from gamerraterapi.views import GameViewSet, GameImageViewSet, UserViewSet

from gamerraterapi.views.category import CategoryViewSet
from gamerraterapi.views.game_rating import RatingViewSet
from gamerraterapi.views.game_review import GameReviewViewSet
from gamerraterproject import settings
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"games", GameViewSet, "game")
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"images", GameImageViewSet, basename="image")
router.register(r"game-reviews", GameReviewViewSet, basename="review")
router.register(r"game-ratings", RatingViewSet, basename="rating")

urlpatterns = [
    path("", include(router.urls)),
    path("login", UserViewSet.as_view({"post": "user_login"}), name="login"),
    path(
        "register", UserViewSet.as_view({"post": "register_account"}), name="register"
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
