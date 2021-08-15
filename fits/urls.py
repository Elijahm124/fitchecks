from django.urls import path
from . import views

app_name = 'fits'
urlpatterns = [
    path('', views.index, name='index'),
    path('<owner>/new_fit', views.new_fit, name='new_fit'),
    path('<owner>/closets', views.closets, name='closets'),
    path('<owner>', views.closets, name="closets"),
    path('<owner>/closets/new_closet', views.new_closet, name='new_closet'),
    path('<owner>/<shown_id>', views.fit, name='fit'),
    path('<owner>/closets/<style>/delete', views.delete_closet, name='delete_closet'),
    path('<owner>/closets/<style>', views.closet, name='single_closet'),
    path('<owner>/<shown_id>/delete', views.delete_fit, name='delete_fit'),
    path('<owner>/<shown_id>/edit', views.edit_fit, name='edit_fit'),
    path('<owner>/closets/<style>/remove', views.remove_fits, name='remove_fits'),
    path('<owner>/closets/<style>/add', views.add_fits, name="add_fits"),





]
