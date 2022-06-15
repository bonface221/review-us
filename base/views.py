from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.views.generic.edit import CreateView
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from .models import  Post , Rating 
from django.http import HttpResponseRedirect
from .forms import PostForm,UpdateUserProfileForm,RatingsForm,UpdateUserForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required




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



def home(request):
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post=form.save(commit=False)
            post.user=request.user
            post.save()
        else:
            print('not-valid')
    posts = Post.objects.all()
    form = PostForm()
    context=dict(form=form,posts=posts)

    return render(request,'base/home.html',context)

@login_required(login_url=('login'))
def edit_profile(request,username):
    user = User.objects.get(username=username)
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        prof_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and prof_form.is_valid():
            user_form.save()
            prof_form.save()
            return redirect('profile', user.username)
    else:
        user_form = UpdateUserForm(instance=request.user)
        prof_form = UpdateUserProfileForm(instance=request.user.profile)
    params = {
        'user_form': user_form,
        'prof_form': prof_form
    }
    return render(request, 'base/edit.html', params)

@login_required(login_url=('login'))
def project(request, post):
    post = Post.objects.get(title=post)
    ratings = Rating.objects.filter(user=request.user, post=post).first()
    rating_status = None
    if ratings is None:
        rating_status = False
    else:
        rating_status = True
    if request.method == 'POST':
        form = RatingsForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.user = request.user
            rate.post = post
            rate.save()
            post_ratings = Rating.objects.filter(post=post)

            design_ratings = [d.design for d in post_ratings]
            design_average = sum(design_ratings) / len(design_ratings)

            usability_ratings = [us.usability for us in post_ratings]
            usability_average = sum(usability_ratings) / len(usability_ratings)

            content_ratings = [content.content for content in post_ratings]
            content_average = sum(content_ratings) / len(content_ratings)

            score = (design_average + usability_average + content_average) / 3
            print(score)
            rate.design_average = round(design_average, 2)
            rate.usability_average = round(usability_average, 2)
            rate.content_average = round(content_average, 2)
            rate.score = round(score, 2)
            rate.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = RatingsForm()
    params = {
        'post': post,
        'rating_form': form,
        'rating_status': rating_status

    }
    return render(request, 'project.html', params)

@login_required(login_url=('login'))
def profile(request, username):
    user=User.objects.get(username=username)
    context=dict(user=user)
    return render(request, 'base/profile.html',context)