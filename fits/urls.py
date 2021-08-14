from django.urls import path
from . import views

app_name = 'fits'
urlpatterns = [
    path('', views.index, name='index'),
    path('<owner>/new_fit', views.new_fit, name='new_fit'),
    path('<owner>/closets', views.closets, name='closets'),
    path('<owner>', views.closets, name="closets"),
    path('<owner>/closets/new_closet', views.new_closet, name='new_closet'),
    path('<owner>/<fit_id>', views.fit, name='fit'),
    path('<owner>/closets/<style>', views.closet, name='single_closet'),

]
