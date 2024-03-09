from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from recommender.models import Movie, Rating
from recommender.utils.item_based_filtering import RecommendedData


class UserLoginSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    email = serializers.CharField()


class UserRegisterSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    def validate_password(self, value: str) -> str:
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))

        return value


class MovieSerializer(serializers.Serializer):
    class Meta:
        model = Movie
        fields = ("movieId", "title", "genres")

    movieId = serializers.IntegerField()
    title = serializers.CharField()
    genres = serializers.CharField()


class RecommendedSerializer(serializers.Serializer):
    class Meta:
        model = RecommendedData

    movie = MovieSerializer(read_only=True)
    rating = serializers.FloatField()


class RatingSerializer(serializers.Serializer):
    class Meta:
        model = Rating
        fields = ("id", "movie", "userId", "rating", "timestamp")

    id = serializers.IntegerField()
    movie = MovieSerializer(read_only=True)
    userId = serializers.IntegerField()
    rating = serializers.DecimalField(max_digits=5, decimal_places=2)
    timestamp = serializers.IntegerField()


class NewRatingSerializer(serializers.Serializer):
    class Meta:
        model = Rating
        fields = ("movieId", "userId", "rating")

    movieId = serializers.IntegerField()
    userId = serializers.IntegerField()
    rating = serializers.DecimalField(max_digits=5, decimal_places=2)


class AvgRatingSerializer(serializers.Serializer):
    class Meta:
        model = Rating
        fields = ("id", "movie", "userId", "rating", "timestamp", "avg_rating")

    id = serializers.IntegerField()
    movie = MovieSerializer(read_only=True)
    userId = serializers.IntegerField()
    rating = serializers.DecimalField(max_digits=5, decimal_places=2)
    timestamp = serializers.IntegerField()
    avg_rating = serializers.DecimalField(max_digits=5, decimal_places=2)
