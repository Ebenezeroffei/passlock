from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.views.generic import View
from django.http import HttpResponseRedirect,JsonResponse
from django.contrib.auth.models import User
from .forms import NewUserForm
from .models import ProfilePic

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
            user = get_object_or_404(User,username = username)
            pp = ProfilePic(user = user)
            pp.save()
            messages.success(request,f"Welcome {username}")
            return HttpResponseRedirect(reverse('passlock:home'))
        return render(request,self.template_name,context)
    
    
class GetProfilePicView(View):
    def get(self,request):
        username = request.GET.get('username',None);
        data = {}
        try:
            user = User.objects.get(username = username)
            pp = user.profilepic
            data['image_url'] = pp.profile.url
        except User.DoesNotExist:
            data['image_url'] = None
        
        return JsonResponse(data)
        
