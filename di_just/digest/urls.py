from django.urls import path
from digest import views
from digest.views import *

urlpatterns = [
    path('img-digest/image/update/<int:pk>/', DigestImagesUpdateAPI.as_view(), name='update-img'),
    path('img-digest/image/<int:pk>/', DigestImagesRetrieveDeleteAPI.as_view(), name='retrieve-delete-img'),
    path('img-digest/image/create/', DigestImageCreateAPI.as_view(), name='create-img'),
    path('img-digest/create/', ImageDigestCreateAPI.as_view(), name='create-img-digest'),
    path('img-digest/update/<int:pk>/', ImageDigestUpdateAPI.as_view(), name='update-img-digest'),
    path('img-digest/get/<int:pk>/', ImageDigestRetrieveAPI.as_view(), name='retrieve-img-digest'),
    path('img-digest/delete/<int:pk>/', ImageDigestDeleteAPI.as_view(), name='delete-img-digest'),
    path('img-digest/user/<int:pk>/', UserImageDigestRetrieveAPI.as_view(), name='get-user-img-digest'),

    path('digest/comment/create/', CommentCreateAPI.as_view(), name='comment-create'),
    path('digest/comment/update/<int:pk>/', CommentUpdateAPI.as_view(), name='comment-update'),
    path('digest/comment/delete/<int:pk>/', CommentDeleteAPI.as_view(), name='comment-delete'),
    path('digest/comments/', DigestCommentsRetrieveAPI.as_view(), name='digest-comments'),
    path('digest/save/', DigestSaveAPI.as_view(), name='save-digest'),
    path('digest/unsave/', DigestUnsaveAPI.as_view(), name='save-digest'),
    # path('digest/by-topic/', DigestByTopicOrAPI.as_view(), name='digest-by-topic'),

    path('link-digest/create/', LinkDigestCreateAPI.as_view(), name='create-link-digest'),
    path('link-digest/update/<int:pk>/', LinkDigestUpdateAPI.as_view(), name='update-link-digest'),
    path('link-digest/get/<int:pk>/', LinkDigestRetrieveAPI.as_view(), name='get-link-digest'),
    path('link-digest/delete/<int:pk>/', LinkDigestDeleteAPI.as_view(), name='delete-link-digest'),
    path('link-digest/user/<int:pk>/', UserLinkDigestRetrieveAPI.as_view(), name='get-user-link-digest'),

    path('img-all/', ImageDigestListAPI.as_view(), name='img-sorter'),
    path('link-all/', LinkDigestListAPI.as_view(), name='link-sorter')
]
