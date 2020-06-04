from django.urls import path
from . import views as home_views

app_name = 'passlock'
urlpatterns = [
    path('home/',home_views.LandingView.as_view(),name = 'home'),
   path('account/<int:pk>/',home_views.AccountDetailView.as_view(),name = 'account_detail'),
 	path('account/delete/<int:pk>/',home_views.AccountDeleteView.as_view(),name = 'account_delete'),
 	path('account/edit/<int:pk>/',home_views.AccountEditView.as_view(),name = 'account_edit'),
 	path('account/create/',home_views.AccountCreateView.as_view(),name = 'account_create'),
 	path('user/verify/',home_views.VerifyUserView.as_view(),name = 'verify'),
 	path('account/create-custom-field-for-account/',home_views.CreateCustomFieldForAccountView.as_view(),name = 'add_custom_field_to_account'),
 	path('account/extension/create-custom-field-for-account/',home_views.CreateCustomeFieldForAccountExtensionView.as_view(),name = 'extension_add_custom_field_to_account'),
 	path('account/delete-custom-field-for-account/',home_views.DeleteCustomFieldForAccountView.as_view(),name = 'delete_custom_account'),
]