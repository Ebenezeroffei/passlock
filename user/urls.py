from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView
from . import views as user_views

app_name = 'user'
urlpatterns = [
    path('user/signin/',LoginView.as_view(template_name = 'user/signin.html'),name = 'signin'),
    path('user/logout/',LogoutView.as_view(),name = 'logout'),
    path('user/register/',user_views.NewUserView.as_view(),name = 'signup'),
    path('image/url/',user_views.GetProfilePicView.as_view(),name = 'image_url'),
]