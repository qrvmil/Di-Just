from django.contrib import admin

# Register your models here.

from digest.models import LinkDigest, ImageDigest, DigestImages, DigestLinks, Topics, Comments

admin.site.register(LinkDigest)
admin.site.register(ImageDigest)
admin.site.register(DigestLinks)
admin.site.register(DigestImages)
admin.site.register(Topics)
admin.site.register(Comments)