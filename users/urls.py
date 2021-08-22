from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('login', auth_views.LoginView.as_view(template_name="registration/login.html",
                                               redirect_authenticated_user=True), name='login'),
    path('register', views.register, name='register'),
    path()
]
