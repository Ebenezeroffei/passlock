from django.shortcuts import render,get_object_or_404
from django.views import generic
from django.http import JsonResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
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
		context = {}
		if request.method == 'POST':
			account_name = request.POST.get('account_name',None)
			user = request.user
			accounts = [account[2] for account in user.account_set.values_list()]
			if account_name not in accounts:
				account = Account(user = user,account_name = account_name)
				account.save()
			
				return HttpResponseRedirect(reverse('passlock:account_edit',kwargs = {'pk':account.pk}))
			messages.error(request,'There account you are trying to create already exists')
			context['acc'] = account_name
			
		return render(request,self.template_name,context)
	

class AccountEditView(generic.View):
	template_name = 'home/account_form.html'
	
	@method_decorator(login_required)
	def dispatch(self,request,*args,**kwargs):
		account_id = int(self.kwargs.get('pk'))
		account = get_object_or_404(Account,id = account_id)
		context = {'object':account}
		if request.method == 'POST':
			account_name = request.POST.get('account_name')
			account.account_name = account_name
			account.date_modified = timezone.now()
			account.save()
			# Get the values in the custom fields
			custom_account_data = [ value for key,value in request.POST.items() if key.startswith('custom_field')]
			# Modify and save the values in the custom fields
			for num,custom in enumerate(account.customfieldsforaccount_set.all()):
				custom.field_value = custom_account_data[num]
				custom.save()
			custom = [c.field_value for c in account.customfieldsforaccount_set.all()]
			# Redirect to the detail page
			return HttpResponseRedirect(reverse('passlock:account_detail',kwargs = {'pk':account.pk}))
			
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
		encrypted_field_value = request.GET.get("value",None)
		# Get the encrypted field value
		values = encrypted_field_value.split('-')[0]
		keys = encrypted_field_value.split('-')[1]
		field_value = ""
		count = 0
		# Decrypt it
		for i in keys:
			if count < len(values):
				field_value += values[count]
				count += int(i) + 1
			
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
	
class CreateCustomeFieldForAccountExtensionView(generic.View):
	""" This class saves customs fields to an account when a user saves an account using the app's extension """
	def get(self,request,*args,**kwargs):
		username = request.GET.get('username',None)
		account_name = request.GET.get('accountName',None)
		field_name = request.GET.get('fieldName',None)
		field_type = request.GET.get('fieldType',None)
		encrypted_field_value = request.GET.get('fieldValue',None)
		# Get the encrypted field value
		values = encrypted_field_value.split('-')[0]
		keys = encrypted_field_value.split('-')[1]
		field_value = ""
		count = 0
		# Decrypt it
		for i in keys:
			if count < len(values):
				field_value += values[count]
				count += int(i) + 1
		# Get the user
		user = User.objects.get(username = username)
		# Get the user's accounts
		all_accounts = user.account_set.values_list('account_name')
		# Filter the user's account
		all_accounts = [x[0] for x in all_accounts]
		if not account_name in all_accounts:
			account = Account(account_name = account_name.capitalize(),user = user)
			account.save()
		account_id = user.account_set.get(account_name = account_name).id
		account = get_object_or_404(Account,id = account_id)
		custom = CustomFieldsForAccount(
			account = account,
			field_name = field_name.capitalize(),
			field_type = field_type,
			field_value = field_value
		)
		custom.save()
		data = {}
		
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