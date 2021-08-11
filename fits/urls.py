from django.urls import path
from . import views

app_name = 'fits'
urlpatterns = [
    path('', views.index, name='index'),
    path('<owner>/closets/<style>', views.closet, name='closet'),
]