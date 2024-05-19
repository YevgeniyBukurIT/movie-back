from rest_framework import generics
from movies.serializes import *
from movies.models import *
from movies.permissions import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.db.models import Avg
import random


class MovieListView(generics.ListAPIView):
    serializer_class = MovieListSerializer

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False)
        genre_name = self.request.query_params.get('genre')
        category_name = self.request.query_params.get('category')
        type_movie_name = self.request.query_params.get('type_movie')
        title = self.request.query_params.get('title')

        if title:
            movies = movies.filter(title=title)

        if category_name:
            category = Category.objects.filter(name=category_name).first()
            if category:
                movies = movies.filter(category=category)

        if genre_name:
            genre = Genre.objects.filter(name=genre_name).first()
            if genre:
                movies = movies.filter(genres=genre)

        if type_movie_name:
            type_movie = MovieType.objects.filter(type=type_movie_name).first()
            if type_movie:
                movies = movies.filter(type=type_movie)

        return movies


class MovieDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MovieDetailSerializer
    queryset = Movie.objects.filter(draft=False)
    permission_classes = (ReadOnly, IsAuthenticated)


class GenreListView(generics.ListAPIView):
    serializer_class = GenreListSerializer
    queryset = Genre.objects.all()


class GenreDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GenreDetailSerializer
    queryset = Genre.objects.all()
    permission_classes = (ReadOnly, IsAuthenticated)


class CategoryListView(generics.ListAPIView):
    serializer_class = CategoryListSerializer
    queryset = Category.objects.all()


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategoryDetailSerializer
    queryset = Category.objects.all()
    permission_classes = (ReadOnly, IsAuthenticated)


class HistoryMovieView(APIView):
    serializer_class = HistoryMovieSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user_request = self.request.user
        profile_current_user = Profile.objects.filter(user=user_request).first()
        data = HistoryMovie.objects.filter(profile=profile_current_user)
        serializer = HistoryMovieListSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def post(self, request, *args, **kwargs):
        user_request = self.request.user
        profile_current_user = Profile.objects.filter(user=user_request).first()
        serializer = HistoryMovieSerializer(data=request.data)
        if serializer.is_valid():
            HistoryMovie.objects.create(profile=profile_current_user,
                                        movie_id=serializer.data.get('movie'))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewMovieView(APIView):
    serializer_class = ReviewMovieSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        reviews = Review.objects.all()
        movie_id = self.request.query_params.get('movie_id')
        if movie_id is not None:
            reviews = reviews.filter(movie_id=movie_id)
        serializer = ReviewMovieListSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def post(self, request, *args, **kwargs):
        username = self.request.user
        serializer = ReviewMovieSerializer(data=request.data)
        if serializer.is_valid():
            movie_id = serializer.data.get("movie")
            text = serializer.data.get("text")
            parent = serializer.data.get("parent")
            if not parent:
                parent = None
            Review.objects.create(name=username, text=text, parent_id=parent, movie_id=movie_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RatingMovieView(APIView):
    serializer_class = RatingMovieSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        movie_id = self.request.query_params.get('movie_id')
        if not movie_id:
            return Response({"error": "The movie_id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        ratings = Rating.objects.all().filter(movie_id=movie_id)
        average_star = 0
        if len(ratings) != 0:
            average_star = ratings.aggregate(Avg('star'))['star__avg']
        rating_user = ratings.filter(user=self.request.user).first()
        star_user = 0
        if rating_user:
            star_user = float(rating_user.star_id)
        return Response({"rating": average_star,
                         "rating_user": star_user}, status=status.HTTP_201_CREATED)

    def post(self, request, *args, **kwargs):
        serializer = RatingMovieSerializer(data=request.data)
        if serializer.is_valid():
            movie_id = serializer.data.get("movie")
            star_id = serializer.data.get("star")
            current_user = User.objects.filter(username=self.request.user).first()
            ratings_current_user = Rating.objects.filter(user=self.request.user)
            ratings_current_movie = ratings_current_user.filter(movie_id=movie_id)
            if ratings_current_movie.first():
                ratings_current_movie.update(star_id=star_id)
            else:
                Rating.objects.create(star_id=star_id, movie_id=movie_id, user_id=current_user.pk)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        profile_current_user = Profile.objects.filter(user=self.request.user).first()
        if not profile_current_user:
            current_user = User.objects.filter(username=self.request.user).first()
            profile_current_user = Profile.objects.create(user_id=current_user.pk)
        serializer = ProfileSerializer(profile_current_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def post(self, request, *args, **kwargs):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            profiles_current_user = Profile.objects.filter(user=self.request.user)
            current_user = User.objects.filter(username=self.request.user).first()
            if not profiles_current_user.first():
                Profile.objects.create(user_id=current_user.pk, **serializer.data)
            else:
                profiles_current_user.update(**serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TechnicalSupportUserView(APIView):
    serializer_class = TechnicalSupportUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = TechnicalSupportUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecommendationsView(generics.ListAPIView):
    serializer_class = MovieListSerializer

    def get_queryset(self):
        random_movies = Movie.objects.filter(draft=False)
        if len(random_movies) > 10:
            random_movies = random.sample(list(random_movies), 10)
        return random_movies


class VideoView(generics.ListAPIView):
    serializer_class = VideoSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        movie_id = self.request.query_params.get('movie_id')
        if movie_id is not None:
            return Video.objects.filter(movie_id=movie_id)
        return []


class GroupMovieView(APIView):
    serializer_class = GroupMovieSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        groups = Group.objects.all()
        serializer = GroupMovieListSerializer(groups, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def post(self, request, *args, **kwargs):
        serializer = GroupMovieSerializer(data=request.data)
        if serializer.is_valid():
            current_profile = Profile.objects.filter(user=self.request.user).first()
            Group.objects.create(owner=current_profile, **serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupSubscribeMovieView(APIView):
    serializer_class = GroupSubscribeSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        current_profile = Profile.objects.filter(user=self.request.user).first()
        groups = Group.objects.all().filter(subscribers=current_profile)
        serializer = GroupMovieListSerializer(groups, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def post(self, request, *args, **kwargs):
        serializer = GroupSubscribeSerializer(data=request.data)
        if serializer.is_valid():
            current_profile = Profile.objects.filter(user=self.request.user).first()
            id_group = self.request.query_params.get('id')
            group = Group.objects.filter(id=id_group).first()
            if not group:
                return Response({"error": "The id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
            is_sub = group.subscribers.filter(id=current_profile.pk).first()
            if not is_sub:
                group.subscribers.add(current_profile.pk)
            else:
                group.subscribers.remove(current_profile.pk)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecommendationMoviesByGroupsView(generics.ListAPIView):
    serializer_class = HistoryMovieListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        current_profile = Profile.objects.filter(user=self.request.user).first()
        groups = Group.objects.all().filter(subscribers=current_profile)
        list_history_movie = []
        for group in groups:
            for profile_user in group.subscribers.values():
                list_history_movie += HistoryMovie.objects.filter(profile_id=profile_user.get('id'))

        if len(list_history_movie) > 10:
            list_history_movie = random.sample(list(list_history_movie), 10)
        return list_history_movie
