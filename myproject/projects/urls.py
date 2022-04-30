from __future__ import unicode_literals
from . import views
from django.urls import path, re_path

urlpatterns = [
    
    path('', views.project, name='projects'),

    path('project/<str:title>/', views.single_project, name='single_project'),

    path('create-project/', views.create_project, name='create-project'),

    path('update-project/<str:pk>/', views.updateProject, name='update-project'),

    path('delete-project/<str:pk>/', views.deleteProject, name='delete-project'),

]