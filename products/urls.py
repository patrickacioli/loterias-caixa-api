from django.urls import path
from . import views

urlpatterns = [
    path("", views.home),
    path("process", views.process),
    path("api/<str:contest>", views.api)    
]
