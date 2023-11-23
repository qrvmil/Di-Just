from django.db import models
from django.contrib.auth.models import User


# в данном файле представлены модели для работы с базой данных

class Topics(models.Model):
    AVAILABLE = [
        ("Art", "AR"),
        ("Sport", "SP"),
        ("Computer Science", "CS"),
        ("Math", "MTH"),
        ("News", "NW"),
        ("Education", "ED"),
        ("Food", "FD"),
        ("Travelling", "TRV"),
        ("Animals", "AN"),
        ("Memes", "MS"),
        ("Technologies", "TCH"),
        ("Music", "MSC"),
        ("Cinema", "CN"),
    ]
    topic_name = models.CharField(max_length=30, choices=AVAILABLE, unique=True)

    def __str__(self):
        return f'{self.topic_name}'


class ImageDigest(models.Model):
    owner = models.ForeignKey('user.Profile', blank=True, null=True, on_delete=models.CASCADE,
                              related_name='created_img_digest')
    introduction = models.TextField(blank=True)
    name = models.CharField(max_length=50)
    topic = models.ManyToManyField(Topics, blank=True, related_name='image_digest')
    conclusion = models.TextField(blank=True)
    saves = models.ManyToManyField('user.Profile', blank=True, null=True, related_name='saved_img_digest')
    public = models.BooleanField(default=True)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'


class LinkDigest(models.Model):
    owner = models.ForeignKey('user.Profile', blank=True, null=True, on_delete=models.CASCADE,
                              related_name='created_link_digest')
    introduction = models.TextField(blank=True)
    name = models.CharField(max_length=50)
    topic = models.ManyToManyField(Topics, blank=True, related_name='link_digest')
    conclusion = models.TextField(blank=True)
    saves = models.ManyToManyField('user.Profile', blank=True, null=True, related_name='saved_link_digest')
    public = models.BooleanField(default=True)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'


class DigestImages(models.Model):
    digest = models.ForeignKey(ImageDigest, on_delete=models.CASCADE, related_name='images', null=True)
    picture = models.ImageField(upload_to="digest_images", blank=True)
    description = models.TextField()

    # данная функция отвечает за удаление картинки дайджеста на сервере, при удалении самого дайджеста
    def delete(self, using=None, keep_parents=False):
        storage, path = self.picture.storage, self.picture.path
        super(DigestImages, self).delete()
        storage.delete(path)

    def __str__(self):
        return f'relate to [{self.digest.name}]'


class DigestLinks(models.Model):
    digest = models.ForeignKey(LinkDigest, on_delete=models.CASCADE, related_name='links', null=True)
    link = models.URLField(blank=True)
    description = models.TextField()

    def __str__(self):
        return f'relates to [{self.digest.name}]'


class Comments(models.Model):
    user = models.ForeignKey('user.Profile', on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    link_digest = models.ForeignKey(LinkDigest, on_delete=models.CASCADE, related_name='comments', null=True,
                                    blank=True)
    img_digest = models.ForeignKey(ImageDigest, on_delete=models.CASCADE, related_name='comments', null=True,
                                   blank=True)
