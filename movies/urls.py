from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('get_movies', SearchMovie.as_view(), name='get_movie'),
    path('movie/', DetailMovie.as_view(), name='movie_detail'),
    path('add_bookmark', AddBookmark.as_view(), name='add_bookmark'),
    path('remove_bookmark', RemoveBookmark.as_view(), name='remove_bookmark'),

]
