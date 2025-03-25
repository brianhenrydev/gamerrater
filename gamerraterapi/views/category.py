from django.contrib import auth
from gamerraterapi.models.category import Category
from gamerraterapi.views.user import UserSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "label"]


class CategoryViewSet(viewsets.ViewSet):
    def list(self, request):
        categorys = Category.objects.all()
        serializer = CategorySerializer(
            categorys, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)
        except category.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        label = request.data.get("label")

        category = Category.objects.create(label=label)

        serialized = CategorySerializer(category, context={"request": request})
        return Response(serialized.data, status=status.HTTP_201_CREATED)
