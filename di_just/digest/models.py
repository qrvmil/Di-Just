from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Topics(models.Model):
    AVAILABLE = [
        ("AR", "Art"),
        ("SP", "Sport"),
        ("CS", "Computer Science"),
        ("MTH", "Math"),
        ("NW", "News"),
        ("ED", "Education"),
        ("FD", "Food"),
        ("TRV", "Travelling"),
        ("AN", "Animals"),
        ("MS", "Memes"),
        ("TCH", "Technologies"),
        ("MSC", "Music"),
        ("CN", "Cinema"),
    ]
    topic_name = models.CharField(max_length=30, choices=AVAILABLE)

    def __str__(self):
        return f'{self.topic_name}'


class ImageDigest(models.Model):
    owner = models.ForeignKey('user.Profile', blank=True, null=True, on_delete=models.CASCADE,
                              related_name='created_img_digest')
    introduction = models.TextField(blank=True)
    name = models.CharField(max_length=50)
    topic = models.ManyToManyField(Topics, blank=True)
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
    topic = models.ManyToManyField(Topics, blank=True)
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

    def __str__(self):
        return f'relate to [{self.digest.name}]'


class DigestLinks(models.Model):
    digest = models.ForeignKey(LinkDigest, on_delete=models.CASCADE, related_name='links', null=True)
    link = models.URLField(blank=True)
    description = models.TextField()

    def __str__(self):
        return f'relate to [{self.digest.name}]'


class Comments(models.Model):
    user = models.ForeignKey('user.Profile', on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    link_digest = models.ForeignKey(LinkDigest, on_delete=models.CASCADE, related_name='comments', null=True,
                                    blank=True)
    img_digest = models.ForeignKey(ImageDigest, on_delete=models.CASCADE, related_name='comments', null=True,
                                   blank=True)
