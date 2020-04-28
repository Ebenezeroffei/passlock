from django.shortcuts import render,get_object_or_404
from django.views import generic
from django.http import JsonResponse,HttpResponseRedirect
from django.contrib.auth import authenticate
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .encryption_decryption import Encryption,Decryption
from .models import DefaultAccount,CustomFieldsForDefaultAccount






# Create your views here.
class LandingView(LoginRequiredMixin,generic.ListView):
    model = DefaultAccount
    template_name = 'home/index.html'
    context_object_name = 'accounts'
    
    def get_queryset(self,*args,**kwargs):
        queryset = DefaultAccount.objects.filter(user = self.request.user)
		
        return queryset

class DefaultAccountDetailView(LoginRequiredMixin,generic.DetailView):
	model = DefaultAccount
	
class DefaultAccountCreateView(LoginRequiredMixin,generic.CreateView):
	model = DefaultAccount
	fields = ['account_name','email','password']
	template_name = 'home/defaultaccount_form.html'
	
	def form_valid(self,form,*args,**kewargs):
		form.instance.user = self.request.user
		return super().form_valid(form)
	
class DefaultAccountEditView(LoginRequiredMixin,generic.UpdateView):
	model = DefaultAccount
	fields = ['account_name','email','password']
	template_name = 'home/defaultaccount_form.html'
	
	
	
class DefaultAccountDeleteView(generic.View):
	""" This class deletes a default account """
	def dispatch(self,request,*args,**kwargs):
		account_id = self.kwargs.get('pk')
		account = get_object_or_404(DefaultAccount,id = account_id)
		account.delete()
		
		return HttpResponseRedirect(reverse('passlock:home'))
	
	
	
class VerifyUserView(generic.View):
	""" This verfies an existing user before he or she edits an account """
	def get(self,request):
		password = request.GET.get('password',None)
		username = request.user.username
		authenticate_user = authenticate(username = username,password = password)
		data = {}
		
		data['user_status'] = True if authenticate_user else False
		return JsonResponse(data)

class CreateCustomFieldForDefaultAccountView(generic.View):
	""" This class creates a new custom field for a default account """
	
	def get(self,request,*args,**kwargs):
		field_name = request.GET.get("name",None)
		field_type = request.GET.get("type",None)
		field_value = request.GET.get("value",None)
		account_id = int(request.GET.get("accountId",None))
		account = get_object_or_404(DefaultAccount,id = account_id)
		custom = CustomFieldsForDefaultAccount(
			default_account = account,
			field_name = field_name,
			field_type = field_type,
			field_value = field_value,
		)
		custom.save()
		
		
		data = {
			'custom_account_id': custom.id,
		}
		return JsonResponse(data)
	
class DeleteCustomFieldForDefaultAccountView(generic.View):
	""" This class removes a custom field from a default account """
	def get(self,request,*args,**kwargs):
		# Use the id of the custom account to find the custom account
		custom_account_id = int(request.GET.get('customAccountId',None))
		custom_account = get_object_or_404(CustomFieldsForDefaultAccount,id = custom_account_id)
		# Delete if from the database
		custom_account.delete()
		data = {}
		
		return JsonResponse(data)