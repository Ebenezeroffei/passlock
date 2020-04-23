from django.shortcuts import render
from django.views import generic
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .encryption_decryption import Encryption,Decryption
from .models import DefaultAccount






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
	
class DefaultAccountEditView(LoginRequiredMixin,generic.UpdateView):
	model = DefaultAccount
	fields = ['username','password']
	template_name = 'home/defaultaccount_edit.html'
	
	
	
class VerifyUserView(generic.View):
	""" This verfies an existing user before he or she edits an account """
	def get(self,request):
		password = request.GET.get('password',None)
		username = request.user.username
		authenticate_user = authenticate(username = username,password = password)
		data = {}
		
		data['user_status'] = True if authenticate_user else False
		return JsonResponse(data)