from django.urls import path

from movies.views import *

urlpatterns = [
    path('movie/all/', MovieListView.as_view()),
    path('movie/<int:pk>/', MovieDetailView.as_view()),
    path('genre/all/', GenreListView.as_view()),
    path('genre/<int:pk>/', GenreDetailView.as_view()),
    path('category/all/', CategoryListView.as_view()),
    path('category/<int:pk>/', CategoryDetailView.as_view()),
    path('movie/history/', HistoryMovieView.as_view()),
    path('movie/review/', ReviewMovieView.as_view()),
    path('movie/rating/', RatingMovieView.as_view()),
    path('movie/recommend/', RecommendationsView.as_view()),
    path('movie/video/', VideoView.as_view()),
    path('user/profile/', ProfileView.as_view()),
    path('technicalsupport/', TechnicalSupportUserView.as_view()),
    path('groups/', GroupMovieView.as_view()),
    path('groups/subscribe/', GroupSubscribeMovieView.as_view()),
    path('groups/recomend/movie/', RecommendationMoviesByGroupsView.as_view()),
]
