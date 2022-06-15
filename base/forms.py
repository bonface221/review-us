

from django import forms
from django.contrib.auth.models import User
from .models import Post, Profile, Rating

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('profile_picture', 'title', 'url', 'description', 'technologies',)

class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email')

class UpdateUserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'location', 'profile_picture', 'bio', 'contact']


class RatingsForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['design', 'usability', 'content']