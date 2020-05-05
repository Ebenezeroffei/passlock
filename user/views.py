from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.views.generic import View
from django.http import HttpResponseRedirect,JsonResponse
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import NewUserForm,UserProfileEditForm,ProfilePicEditForm
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
        
class UserProfileView(View):
	template_name = 'user/profile.html'
	
	@method_decorator(login_required)
	def dispatch(self,request,*args,**kwargs):
		return render(request,self.template_name)
	
	
class UserProfileEditView(LoginRequiredMixin,View):
	template_name = 'user/profile_edit.html'
	form_class1 = UserProfileEditForm
	form_class2 = ProfilePicEditForm
	
	def get(self,*args,**kwargs):
		form1 = self.form_class1(instance = self.request.user)
		form2 = self.form_class2(instance = self.request.user.profilepic)
		context = {
			'u_form':form1,
			'p_form':form2,
		}
		return render(self.request,self.template_name,context)
	
	def post(self,*args,**kwargs):
		form1 = self.form_class1(self.request.POST,instance = self.request.user)
		form2 = self.form_class2(self.request.POST,self.request.FILES,instance = self.request.user.profilepic)
		context = {
			'u_form':form1,
			'p_form':form2,
		}
		
		if form1.is_valid() and form2.is_valid():
			form1.save()
			form2.save()
			return HttpResponseRedirect(reverse('user:profile'))

		return render(self.request,self.template_name,context)
	
