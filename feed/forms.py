from django import forms
from .models import UserProfile, Post

class ProfileForm(forms.ModelForm):

	class Meta:
		model = UserProfile
		fields = ['photo','phone_no','status']


class PostForm(forms.ModelForm):

	class Meta:
		model = Post
		fields = ['pic','quote']