from django.urls import path
from . import views as home_views

app_name = 'passlock'
urlpatterns = [
    path('home/',home_views.LandingView.as_view(),name = 'home'),
   path('account/<int:pk>/',home_views.DefaultAccountDetailView.as_view(),name = 'default_account_detail'),
 	path('account/edit/<int:pk>/',home_views.DefaultAccountEditView.as_view(),name = 'default_account_edit'),
 	path('user/verify/',home_views.VerifyUserView.as_view(),name = 'verify'),
]