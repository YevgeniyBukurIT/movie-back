1) ```install python3``` https://www.python.org
2) ```cd movie_back```
3) create folder media
4) ```python -m pip install -r requirements.txt```
5) ```python manage.py makemigrations```
6) ```python manage.py migrate```
7) ```python manage.py runserver```
8) server starting - http://127.0.0.1:8000/

for generate tests data:
```python manage.py seed movies --number=15```

for create admin:
```python manage.py createsuperuser```

API:
````
api/v1/movies/movie/all/ - GET
api/v1/movies/movie/{id}/ - GET
api/v1/movies/genre/all/ - GET
api/v1/movies/genre/{id}/ - GET
api/v1/movies/category/all/ - GET
api/v1/movies/category/{id}/ - GET

/api/v1/auth_token/token/login/ - POST 
Body:
{
    "password": "",
    "username": ""
}
/api/v1/auth_token/token/logout/ - POST
/api/v1/auth/users/ - POST (create user)
Body: 
{
    "email": "",
    "username": "",
    "password": ""
}
/api/v1/auth/users/me/ - POST (get info user)

how to pass token in headers - https://i.imgur.com/SVoExBt.png
docs - https://www.django-rest-framework.org/api-guide/authentication/


api/v1/movies/ movie/history/ - GET
api/v1/movies/ movie/history/ - POST
Body: 
{
    "movie": {id}
}
api/v1/movies/ movie/review/?movie_id={id} - GET
api/v1/movies/ movie/review/ - POST
Body: 
{
    "movie": {id}
    "text": ""
    parent: {id|null}
}
api/v1/movies/ movie/rating/?movie_id={id} - GET
api/v1/movies/ movie/rating/ - POST
Body: 
{
    "movie": {id}
    "star": {number} //1 - 5
}
api/v1/movies/ movie/recommend/ - GET
api/v1/movies/ movie/video/?movie_id={id} - GET
api/v1/movies/ user/profile/ - GET
api/v1/movies/ user/profile/ - POST
Body: 
{
    "avatar": ""
    "last_name": ""
    "first_name": ""
    "first_name": ""
    "birthday": ""
}
api/v1/movies/ technicalsupport/ - POST
Body: 
{
    "email": ""
    "text": ""
}

api/v1/movies/groups/ - GET
api/v1/movies/groups/ - POST
Body: 
{
    "title": ""
    "image": ""
    "description": ""
}
api/v1/movies/groups/subscribe/ - GET - only subscribe groups 
api/v1/movies/groups/subscribe/?id={id} - POST - if the user is subscribed, then he will unsubscribe to the group; if he is not subscribed, he will sign
api/v1/movies/groups/recomend/movie/ - GET
````