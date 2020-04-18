from django.shortcuts import render
from django.views import generic
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
