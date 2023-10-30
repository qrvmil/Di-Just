from django.urls import path
from user import views
from user.views import *
from digest.views import *
from knox.urls import views as knoxviews


urlpatterns = [
    path('register/', RegisterUserAPI.as_view(), name='register'),
    path('users/update/<int:pk>/', UserUpdateAPI.as_view(), name='user-update'),
    path('users/user/<int:pk>/', UserInfoAPI.as_view(), name='user-info-delete'),
    path('users/profile/restore/email/', ProfileRestoreEmailAPI.as_view(), name='send-email'),
    path('restore/<int:uid>/<str:token>',
         ProfileRestoreAPI.as_view(), name='restore'),
    path('users/profile/update/<int:pk>/', ProfileUpdateAPI.as_view(), name='profile-update'),
    path('users/profile/update/picture/<int:pk>/', ProfilePictureUpdateAPI.as_view(), name='profile-picture-update'),
    path('users/profile/update/password/<int:pk>/', PasswordUpdateAPI.as_view(), name='password-update'),
    path('users/profile/<int:pk>/', ProfileInfoAPI.as_view(), name='profile-info-delete'),
    path('users/profile-info/<int:pk>/', ProfileGetInfo.as_view(), name='get-profile-info'),
    path('users/profiles/', ProfileListAPI.as_view(), name='profiles'),
    path('users/login/', LoginAPI.as_view(), name='login'),
    path('users/logout/', knoxviews.LogoutView.as_view(), name='logout'),
    path('users/follow/<int:pk>/', FollowUserAPI.as_view(), name='follow'),
    path('users/unfollow/<int:pk>/', UnfollowUserAPI.as_view(), name='unfollow'),
    path('users/saved-img-digests/', SavedImageDigestsAPI.as_view(), name='saved-img-digests'),
    path('users/saved-link-digests/', SavedLinkDigestsAPI.as_view(), name='saved-link-digests'),
    path('activate/<int:uid>/<str:token>', ActivateAPI.as_view(),
         name='activate'),

]
