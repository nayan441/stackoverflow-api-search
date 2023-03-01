from django.urls import path, include
from . import views
urlpatterns = [
    path('search/',views.search, name='search02'),
    path('',views.search, name='search'),
]
