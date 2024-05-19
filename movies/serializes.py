from rest_framework import serializers
from movies.models import *
from django.contrib.auth.models import User


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ActorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ('id', 'name')


class ActorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'


class GenreListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name')


class GenreDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class MovieTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieType
        fields = '__all__'


class MovieDetailSerializer(serializers.ModelSerializer):
    genres = GenreListSerializer(many=True)
    directors = ActorListSerializer(many=True)
    actors = ActorListSerializer(many=True)
    category = CategoryListSerializer()
    type = MovieTypeSerializer()

    class Meta:
        model = Movie
        fields = '__all__'


class MovieListSerializer(serializers.ModelSerializer):
    genres = GenreListSerializer(many=True)
    category = CategoryListSerializer()
    type = MovieTypeSerializer()

    class Meta:
        model = Movie
        fields = ('id', 'title', 'poster', 'year', 'genres', 'type', 'category')


class HistoryMovieListSerializer(serializers.ModelSerializer):
    movie = MovieListSerializer()

    class Meta:
        model = HistoryMovie
        fields = ['id', "movie"]


class HistoryMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoryMovie
        fields = ["id", "movie"]


class ReviewMovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "name", "text"]


class ReviewMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["text", "parent", "movie"]


class RatingMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ["star", "movie"]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ["user", "is_subscribe"]


class TechnicalSupportUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicalSupportUser
        fields = "__all__"


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ["title", "video_file"]


class ProfileGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "last_name", "first_name", "avatar"]


class GroupMovieListSerializer(serializers.ModelSerializer):
    subscribers = ProfileGroupSerializer(many=True)
    owner = ProfileGroupSerializer()

    class Meta:
        model = Group
        fields = "__all__"


class GroupMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["title", "image", "description"]


class GroupSubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id"]
