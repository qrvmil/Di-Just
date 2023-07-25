from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to="users_images", blank=True)
    bio = models.TextField(max_length=500, blank=True)
    age = models.IntegerField(default=0, blank=True)
    follows = models.ManyToManyField("self",
                                     related_name="followed_by",
                                     symmetrical=False,
                                     blank=True)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    # NB by default email field in AbstractUser is not unique, check this in POST request.

    def __str__(self):
        return f'{self.user.username}'
