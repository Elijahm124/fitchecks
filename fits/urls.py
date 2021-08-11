from django.urls import path
from . import views

app_name = 'fits'
urlpatterns = [
    path('', views.index, name='index'),
    path('<owner>/closets/<style>', views.closet, name='single_closet'),
    path('<owner>/closets/<style>/<fit_id>', views.fit, name='fit'),
    path('<owner>/closets', views.closets, name='closets'),
    path('<owner>', views.closets, name='closets')
]