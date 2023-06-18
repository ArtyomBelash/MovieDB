from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=50, blank=True, null=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    summary = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    profession = models.CharField(max_length=50, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    image = models.ImageField(null=True, blank=True, upload_to='media/profile_images',
                              default='media/profile_images/cat.jpg')
    created = models.DateTimeField(auto_now_add=True)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False, blank=True)

    class Meta:
        ordering = ['created']
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.user.username






