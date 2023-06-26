from django.db import models

from users.models import Profile


class API(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.name


class Comment(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey('API', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'

    def __str__(self):
        return f'{self.author} - {self.date}'


class Bookmark(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    movie = models.ForeignKey(API, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.user} - {self.movie.name}'

    class Meta:
        unique_together = ('user', 'movie')
