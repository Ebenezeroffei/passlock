from django.urls import path
from . import views as home_views

app_name = 'passlock'
urlpatterns = [
    path('home/',home_views.LandingView.as_view(),name = 'home'),
   path('account/<int:pk>/',home_views.DefaultAccountDetailView.as_view(),name = 'default_account_detail'),
 	path('account/delete/<int:pk>/',home_views.DefaultAccountDeleteView.as_view(),name = 'default_account_delete'),
 	path('account/edit/<int:pk>/',home_views.DefaultAccountEditView.as_view(),name = 'default_account_edit'),
 	path('account/create/',home_views.DefaultAccountCreateView.as_view(),name = 'default_account_create'),
 	path('user/verify/',home_views.VerifyUserView.as_view(),name = 'verify'),
 	path('account/create-custom-field-for-default-account/',home_views.CreateCustomFieldForDefaultAccountView.as_view(),name = 'add_custom_field_to_default_account'),
 	path('account/delete-custom-field-for-default-account/',home_views.DeleteCustomFieldForDefaultAccountView.as_view(),name = 'delete_custom_account'),
]