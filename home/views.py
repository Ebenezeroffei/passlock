from django.shortcuts import render,get_object_or_404
from django.views import generic
from django.http import JsonResponse,HttpResponseRedirect
from django.contrib.auth import authenticate
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .encryption_decryption import Encryption,Decryption
from .models import Account,CustomFieldsForAccount






# Create your views here.
class LandingView(LoginRequiredMixin,generic.ListView):
    model = Account
    template_name = 'home/index.html'
    context_object_name = 'accounts'
    
    def get_queryset(self,*args,**kwargs):
        queryset = Account.objects.filter(user = self.request.user)
		
        return queryset

class AccountDetailView(LoginRequiredMixin,generic.DetailView):
	model = Account
	

class AccountCreateView(generic.View):
	template_name = 'home/account_form.html'
	
	@method_decorator(login_required)
	def dispatch(self,request,*args,**kwargs):
		if request.method == 'POST':
			account_name = request.POST.get('account_name',None)
			account = Account(user = request.user,account_name = account_name)
			account.save()
			
			return HttpResponseRedirect(reverse('passlock:account_edit',kwargs = {'pk':account.pk}))
			
		return render(request,self.template_name)
	

class AccountEditView(generic.View):
	template_name = 'home/account_form.html'
	
	@method_decorator(login_required)
	def dispatch(self,request,*args,**kwargs):
		account_id = int(self.kwargs.get('pk'))
		account = get_object_or_404(Account,id = account_id)
		context = {'object':account}
		
		return render(request,self.template_name,context)
	
	
	
class AccountDeleteView(generic.View):
	""" This class deletes a default account """
	def dispatch(self,request,*args,**kwargs):
		account_id = self.kwargs.get('pk')
		account = get_object_or_404(Account,id = account_id)
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

class CreateCustomFieldForAccountView(generic.View):
	""" This class creates a new custom field for a default account """
	
	def get(self,request,*args,**kwargs):
		field_name = request.GET.get("name",None)
		field_type = request.GET.get("type",None)
		field_value = request.GET.get("value",None)
		account_id = int(request.GET.get("accountId",None))
		account = get_object_or_404(Account,id = account_id)
		custom = CustomFieldsForAccount(
			account = account,
			field_name = field_name.capitalize(),
			field_type = field_type,
			field_value = field_value,
		)
		custom.save()
		
		
		data = {
			'custom_account_id': custom.id,
		}
		return JsonResponse(data)
	
class DeleteCustomFieldForAccountView(generic.View):
	""" This class removes a custom field from a default account """
	def get(self,request,*args,**kwargs):
		# Use the id of the custom account to find the custom account
		custom_account_id = int(request.GET.get('customAccountId',None))
		custom_account = get_object_or_404(CustomFieldsForAccount,id = custom_account_id)
		# Delete if from the database
		custom_account.delete()
		data = {}
		
		return JsonResponse(data)