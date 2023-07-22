from django.urls import path
from user import views

urlpatterns = [
    path('profiles/', views.profiles_list),
    path('profiles/<int:pk>/', views.profile_detail),
]
