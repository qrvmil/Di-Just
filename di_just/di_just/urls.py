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
from user.views import RegisterUser, UserUpdate, PasswordUpdate, ProfileUpdate, ProfileInfo, UserInfo, ProfileList

# TO DO: make url patterns with the usage of include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('user.urls')),
    # path('', include('digest.urls')),
    path('register/', RegisterUser.as_view(), name='register'),
    path('users/update/<int:pk>/', UserUpdate.as_view(), name='user-update'),
    path('users/user/<int:pk>', UserInfo.as_view(), name='user-info-delete'),
    path('users/update/password/<int:pk>/', PasswordUpdate.as_view(), name='password-update'),
    path('users/profile/update/<int:pk>/', ProfileUpdate.as_view(), name='profile-update'),
    path('users/profile/<int:pk>/', ProfileInfo.as_view(), name='profile-info-delete'),
    path('users/profiles/', ProfileList.as_view(), name='profiles')
]
