from django.shortcuts import render
from django.views import generic

# Create your views here.
class LandingView(generic.View):
    template_name = 'home/index.html'
    
    def dispatch(self,request):
        return render(request,self.template_name)
