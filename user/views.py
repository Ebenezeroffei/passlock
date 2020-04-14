from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.views.generic import View
from django.http import HttpResponseRedirect
from .forms import NewUserForm

# Create your views here.

class NewUserView(View):
    form_class = NewUserForm
    template_name = 'user/signup.html'
    
    def get(self,request,*args,**kwargs):
        form = self.form_class()
        context = {
            'form':form,
        }
        return render(request,self.template_name,context)
    
    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        context = {
            'form':form,
        }
        if form.is_valid():
            username = form.cleaned_data.get('username')
            form.save()
            messages.success(request,f"Welcome {username}")
            return HttpResponseRedirect(reverse('passlock:home'))
        return render(request,self.template_name,context)
