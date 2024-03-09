from django.db import IntegrityError
from datetime import datetime
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, parser_classes
from recommender.models import Rating
from recommender.serializers import (
    NewRatingSerializer,
    RatingSerializer,
    RecommendedSerializer,
    UserRegisterSerializer,
)
from recommender.utils.item_based_filtering import findForUser


@api_view(["POST"])
def save_rating(request: Request) -> Response:
    data = JSONParser().parse(request)
    serializer = NewRatingSerializer(data=data)

    if serializer.is_valid() and isinstance(serializer.validated_data, dict):
        try:
            rating, _ = Rating.objects.update_or_create(
                userId=serializer.validated_data.get("userId"),
                movie_id=serializer.validated_data.get("movieId"),
                defaults={
                    "rating": serializer.validated_data.get("rating"),
                },
                create_defaults={
                    "rating": serializer.validated_data.get("rating"),
                    "timestamp": datetime.now().strftime("%s"),
                },
            )

            new_rating = RatingSerializer(rating)

            return Response(
                {
                    "success": True,
                    "error": False,
                    "data": new_rating.data,
                }
            )
        except IntegrityError as e:
            print(e)
            return Response(
                {
                    "success": False,
                    "error": "Could not save rating",
                    "data": None,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_prev_ratings(req: Request) -> Response:
    userId = req.query_params.get("userId")

    if userId is None:
        return Response(
            {"success": False, "error": "userId is required", "data": None},
            status=status.HTTP_400_BAD_REQUEST,
        )

    ratings = Rating.objects.filter(userId=userId).order_by("timestamp")

    serializer = RatingSerializer(ratings, many=True)

    return Response(
        {
            "success": True,
            "error": None,
            "data": serializer.data,
        },
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
def get_recommendations_for(req: Request) -> Response:
    userId = req.query_params.get("userId")

    if userId is None:
        return Response(
            {"success": False, "error": "userId is required", "data": None},
            status=status.HTTP_400_BAD_REQUEST,
        )

    data = findForUser(int(userId))
    serializer = RecommendedSerializer(data, many=True)

    return Response(
        {
            "success": True,
            "error": None,
            "data": serializer.data,
        },
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@parser_classes([JSONParser])
def sign_up(request: Request) -> Response:
    data = JSONParser().parse(request)
    serializer = UserRegisterSerializer(data=data)

    if serializer.is_valid() and isinstance(serializer.validated_data, dict):
        try:
            user = User.objects.create_user(
                username=serializer.validated_data.get("email").__str__(),
                email=serializer.validated_data.get("email").__str__(),
                password=serializer.validated_data.get("password").__str__(),
                first_name=serializer.validated_data.get("first_name").__str__(),
                last_name=serializer.validated_data.get("last_name").__str__(),
            )

            refresh = RefreshToken.for_user(user)
            access = AccessToken.for_user(user)

            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(access),
                }
            )
        except IntegrityError:
            return Response(
                {"error": "Email already in use"}, status=status.HTTP_400_BAD_REQUEST
            )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
