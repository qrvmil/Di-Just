from django.db import models
from django.contrib.auth.models import User


# модель пользователя
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    picture = models.ImageField(upload_to="users_images", blank=True)
    is_verified = models.BooleanField(default=False)
    bio = models.TextField(max_length=500, blank=True)
    age = models.IntegerField(default=0, blank=True)
    follows = models.ManyToManyField("self",
                                     related_name="followed_by",
                                     symmetrical=False,
                                     blank=True)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    # функция для удаления картинки пользователя на сервере
    def delete(self, using=None, keep_parents=False):
        storage, path = self.picture.storage, self.picture.path
        super(Profile, self).delete()
        storage.delete(path)

    def __str__(self):
        return f'{self.user.username}'
