from django.urls import path
from digest import views

urlpatterns = [
    path('img-digests/', views.img_digest_list),
    path('link-digests/', views.link_digest_list),
]
