from core.models import Tag, Ingredient, Recipe
from rest_framework import serializers


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag object"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """serializer a  recipe"""
    ingredients = serializers.PrimaryKeyRelatedField(many=True, queryset=Ingredient.objects.all())
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'ingredients', 'tags', 'time_minutes', 'price', 'link')
        read_only_fields = ('id',)


class RecipeDetailSerializer(RecipeSerializer):
    """serializer a  recipe details"""
    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)


class RecipeImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading image to recipes"""

    class Meta:
        model = Recipe
        fields = ('id', 'image')
        read_only_fields = ('id',)
