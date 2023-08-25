"""
URL configuration for test_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from user.views import *
from digest.views import *
from knox.urls import views as knoxviews

# TO DO: make url patterns with the usage of include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('user.urls')),
    # path('', include('digest.urls')),

    path('register/', RegisterUser.as_view(), name='register'),
    path('users/update/<int:pk>/', UserUpdate.as_view(), name='user-update'),
    path('users/user/<int:pk>/', UserInfo.as_view(), name='user-info-delete'),
    path('users/profile/restore/email/', ProfileRestoreEmailAPI.as_view(), name='send-email'),
    path('restore/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
         ProfileRestoreAPI.as_view(), name='restore'),
    path('users/profile/update/<int:pk>/', ProfileUpdate.as_view(), name='profile-update'),
    path('users/profile/update/picture/<int:pk>/', ProfilePictureUpdate.as_view(), name='profile-picture-update'),
    path('users/profile/update/password/', PasswordUpdateAPI.as_view(), name='password-update'),
    path('users/profile/<int:pk>/', ProfileInfo.as_view(), name='profile-info-delete'),
    path('users/profiles/', ProfileList.as_view(), name='profiles'),
    path('users/login/', LoginAPI.as_view(), name='login'),
    path('users/logout/', knoxviews.LogoutView.as_view(), name='logout'),
    path('users/follow/<int:pk>/', FollowUser.as_view(), name='follow'),
    path('users/saved-digests/', SavedDigestsAPI.as_view(), name='saved-digests'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', ActivateAPI.as_view(),
         name='activate'),

    path('img-digest/image/update/<int:pk>/', DigestImagesUpdateAPI.as_view(), name='update-img'),
    path('img-digest/image/<int:pk>/', DigestImagesRetrieveDeleteAPI.as_view(), name='retrieve-delete-img'),
    path('img-digest/image/create/', DigestImageCreateAPI.as_view(), name='create-img'),
    path('img-digest/create/', ImageDigestCreateAPI.as_view(), name='create-img-digest'),
    path('img-digest/update/<int:pk>/', ImageDigestUpdateAPI.as_view(), name='update-img-digest'),
    path('img-digest/get/<int:pk>/', ImageDigestRetrieveAPI.as_view(), name='retrieve-img-digest'),
    path('img-digest/delete/<int:pk>/', ImageDigestDeleteAPI.as_view(), name='delete-img-digest'),

    path('digest/comment/create/', CommentCreateAPI.as_view(), name='comment-create'),
    path('digest/comment/update/<int:pk>/', CommentUpdateAPI.as_view(), name='comment-update'),
    path('digest/comment/delete/<int:pk>/', CommentDeleteAPI.as_view(), name='comment-delete'),
    path('digest/comments/', DigestCommentsRetrieveAPI.as_view(), name='digest-comments'),
    path('digest/user/<int:pk>/', UserDigestRetrieveAPI.as_view(), name='get-user-digest'),
    path('digest/save/', DigestSaveAPI.as_view(), name='save-digest'),
    # path('digest/by-topic/', DigestByTopicOrAPI.as_view(), name='digest-by-topic'),

    path('link-digest/create/', LinkDigestCreateAPI.as_view(), name='create-link-digest'),
    path('link-digest/update/<int:pk>/', LinkDigestUpdateAPI.as_view(), name='update-link-digest'),
    path('link-digest/get/<int:pk>/', LinkDigestRetrieveAPI.as_view(), name='get-link-digest'),
    path('link-digest/delete/<int:pk>/', LinkDigestDeleteAPI.as_view(), name='delete-link-digest'),

    path('img-all/', ImageDigestListAPI.as_view(), name='img-sorter'),
    path('link-all/', LinkDigestListAPI.as_view(), name='link-sorter')

]
