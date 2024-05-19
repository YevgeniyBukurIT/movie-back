import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movies_back.settings')

import django
django.setup()

from django_seed import Seed
from pathlib import Path
from django.contrib.auth.models import User
from movies.models import *


seeder = Seed.seeder()

seeder.add_entity(Category, 4, {
    'name': lambda x: seeder.faker.sentence(nb_words=2),
    'description': lambda x: seeder.faker.sentence(nb_words=10)
})

seeder.add_entity(Genre, 4, {
    'name': lambda x: seeder.faker.word(),
    'description': lambda x: seeder.faker.sentence(nb_words=10)
})

seeder.add_entity(Actor, 10, {
    'name': lambda x: seeder.faker.name(),
    'age': lambda x: seeder.faker.random_int(min=18, max=80, step=1),
    'description': lambda x: seeder.faker.sentence(nb_words=20),
    'image': lambda x: Path(seeder.faker.image()),
})

seeder.add_entity(Movie, 30, {
    'title': lambda x: seeder.faker.sentence(nb_words=3),
    'tagline': lambda x: seeder.faker.sentence(nb_words=6),
    'description': lambda x: seeder.faker.sentence(nb_words=20),
    'poster': lambda x: Path(seeder.faker.image()).name,
    'year': lambda x: seeder.faker.random_int(min=1900, max=2022, step=1),
    'country': lambda x: seeder.faker.country(),
    'world_premiere': lambda x: seeder.faker.date_between(start_date='-30y', end_date='today'),
    'budget': lambda x: seeder.faker.random_int(min=1000, max=1000000, step=1000),
    'feed_in_usa': lambda x: seeder.faker.random_int(min=1000, max=1000000, step=1000),
    'feed_in_world': lambda x: seeder.faker.random_int(min=1000, max=1000000, step=1000),
    'category': lambda x: seeder.faker.random_element(Category.objects.all()),
    'draft': lambda x: seeder.faker.boolean(),
})

seeder.add_entity(MovieShots, 30, {
    'title': lambda x: seeder.faker.sentence(nb_words=2),
    'description': lambda x: seeder.faker.sentence(nb_words=10),
    'image': lambda x: Path(seeder.faker.image()),
    'movie': lambda x: seeder.faker.random_element(Movie.objects.all())
})

seeder.add_entity(RatingStar, 10, {
    'value': lambda x: x
})

seeder.add_entity(Rating, 50, {
    'ip': lambda x: seeder.faker.ipv4(),
    'star': lambda x: seeder.faker.random_element(RatingStar.objects.all()),
    'movie': lambda x: seeder.faker.random_element(Movie.objects.all())
})

seeder.add_entity(Review, 20, {
    'email': lambda x: seeder.faker.email(),
    'name': lambda x: seeder.faker.name(),
    'text': lambda x: seeder.faker.sentence(nb_words=30),
    'parent': None,
    'movie': lambda x: seeder.faker.random_element(Movie.objects.all())
})

seeder.add_entity(User, 10, {
    'username': lambda x: seeder.faker.user_name(),
    'email': lambda x: seeder.faker.email(),
    'password': 'password'
})

seeder.add_entity(Profile, 10, {
    'user': lambda x: seeder.faker.random_element(User.objects.all()),
    'first_name': lambda x: seeder.faker.first_name(),
    'last_name': lambda x: seeder.faker.last_name(),
    'phone': lambda x: seeder.faker.phone_number(),
    'birth_date': lambda x: seeder.faker.date_of_birth(),
    'photo': lambda x: Path(seeder.faker.image())
})

seeder.add_entity(HistoryMovie, 50, {
    'user': lambda x: seeder.faker.random_element(User.objects.all()),
    'movie': lambda x: seeder.faker.random_element(Movie.objects.all()),
    'date': lambda x: seeder.faker.date_between(start_date='-30y', end_date='today'),
})

inserted_pks = seeder.execute()
print(inserted_pks)
