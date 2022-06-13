from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.views.generic.edit import CreateView
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm


class SignupView(CreateView):
    form_class=UserCreationForm
    template_name= 'base/registration/register.html'
    success_url='/'

    def get(self,request,*args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().get(request,*args, **kwargs)


def logoutUser(request):
    logout(request)
    return redirect('home')


class LoginInterfaceView(LoginView):
    template_name= 'base/registration/login.html'



class HomeView(TemplateView):
    template_name= 'base/home.html'
    extra_context= dict()


