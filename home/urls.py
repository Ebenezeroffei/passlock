from django.urls import path
from . import views as home_views

app_name = 'passlock'
urlpatterns = [
    path('',home_views.LandingView.as_view(),name = 'home')
]