from django.db import models
from datetime import date
from django.contrib.auth.models import User


class Category(models.Model):
    """Сategories"""
    name = models.CharField("Name", max_length=150)
    description = models.TextField("Description")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Сategories"


class Actor(models.Model):
    """Actors and directors"""
    name = models.CharField("Name", max_length=100)
    age = models.PositiveSmallIntegerField("Age", default=0)
    description = models.TextField("Description")
    image = models.ImageField("Image", upload_to="actors/")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Actors and directors"
        verbose_name_plural = "Actors and directors"


class Genre(models.Model):
    """Genres"""
    name = models.CharField("Name", max_length=100)
    description = models.TextField("Description")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"


class MovieType(models.Model):
    """Movie Type"""

    VIDEO_TYPE_CHOICES = (
        ('movie', 'Movie'),
        ('series', 'Series'),
    )

    type = models.CharField(max_length=10, choices=VIDEO_TYPE_CHOICES)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = "Movie Type"
        verbose_name_plural = "Movie Types"


class Movie(models.Model):
    """Movies"""
    title = models.CharField("Title", max_length=100)
    tagline = models.CharField("Tagline", max_length=100, default='')
    description = models.TextField("Description")
    poster = models.ImageField("Poster", upload_to="movies/")
    year = models.PositiveSmallIntegerField("Year", default=2020)
    country = models.CharField("Country", max_length=30)
    directors = models.ManyToManyField(Actor, verbose_name='Directors', related_name="film_director")
    actors = models.ManyToManyField(Actor, verbose_name="Actors", related_name="film_actor")
    genres = models.ManyToManyField(Genre, verbose_name="Genres")
    world_premiere = models.DateField("World premiere", default=date.today)
    budget = models.PositiveSmallIntegerField("Budget", default=0, help_text="enter the dollar amount")
    feed_in_usa = models.PositiveSmallIntegerField(
        "Amount in USA", default=0, help_text="enter the dollar amount"
    )
    feed_in_world = models.PositiveSmallIntegerField(
        "Amount in World", default=0, help_text="enter the dollar amount"
    )
    category = models.ForeignKey(
        Category, verbose_name='Category', on_delete=models.SET_NULL, null=True
    )
    draft = models.BooleanField("Draft", default=False)
    type = models.ForeignKey(MovieType, verbose_name="MovieType", on_delete=models.CASCADE, null=True)

    def get_review(self):
        return self.review_set.filter(parent__isnull=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = "Movies"


class MovieShots(models.Model):
    """Movie Shots"""
    title = models.CharField("Title", max_length=100)
    description = models.TextField("Description")
    image = models.ImageField("Image", upload_to="movie_shots/")
    movie = models.ForeignKey(Movie, verbose_name="Movie", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Movie Shot"
        verbose_name_plural = "Movie Shots"


class Video(models.Model):
    """Video"""

    title = models.CharField("Title", max_length=100)
    video_file = models.FileField(upload_to='videos/')
    movie = models.ForeignKey(Movie, verbose_name="Movie", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videos"


class RatingStar(models.Model):
    """Rating Star"""
    value = models.SmallIntegerField("Value", default=0)

    def __str__(self):
        return str(self.value)

    class Meta:
        verbose_name = "Rating Star"
        verbose_name_plural = "Rating Stars"


class Rating(models.Model):
    """Rating"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="Star")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="Movie")

    def __str__(self):
        return f"{str(self.star)} - {self.movie}"

    class Meta:
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"


class Review(models.Model):
    """Reviews"""
    name = models.CharField("Name", max_length=100)
    text = models.TextField("Massage", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="Parent", on_delete=models.SET_NULL, blank=True, null=True
    )
    movie = models.ForeignKey(Movie, verbose_name="Movie", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"


class Profile(models.Model):
    """Profiles"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField("Avatar", upload_to='profile_images/', null=True)
    last_name = models.CharField("Last Name", max_length=150, null=True)
    first_name = models.CharField("First Name", max_length=150, null=True)
    phone_number = models.CharField("Phone Number", max_length=12, null=True)
    is_subscribe = models.BooleanField("Subscribe", default=False)
    birthday = models.DateField("Birthday", null=True)

    def __str__(self):
        return self.user.username


class HistoryMovie(models.Model):
    """History Movies"""
    movie = models.ForeignKey(Movie, verbose_name="Movie", on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    profile = models.ForeignKey(Profile, verbose_name="Profile", on_delete=models.CASCADE)

    def __str__(self):
        return self.movie.title


class TechnicalSupportUser(models.Model):
    """Technical Support Users"""
    email = models.EmailField(max_length=254)
    text = models.TextField()

    def __str__(self):
        return self.email


class Group(models.Model):
    """Groups"""
    title = models.CharField("Title", max_length=150)
    image = models.ImageField("Image", upload_to='group_images/', null=True)
    description = models.TextField('Description')
    owner = models.OneToOneField(Profile, on_delete=models.CASCADE)
    subscribers = models.ManyToManyField(Profile, verbose_name="Subscribers", related_name="group_subscribers")

    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"