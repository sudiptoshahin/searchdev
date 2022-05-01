from django.urls import path, re_path
from . import views


urlpatterns = [

    path('login/', views.loginUser, name='login'),

    path('logout/', views.logoutUser, name='logout'),

    path('', views.profile, name='profiles'),

    path('profile/<str:pk>/', views.userProfile, name='user_profile'),


]