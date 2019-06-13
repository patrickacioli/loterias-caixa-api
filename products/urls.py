from django.urls import path
from . import views

urlpatterns = [
    #path("", views.login),
    path("process", views.process),
    path("", views.home),
    path("api/<str:contest>", views.api)    
]
