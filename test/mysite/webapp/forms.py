from django import forms
from .models import Post

from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,
	)

class PostForm(forms.ModelForm): # Post Thread View
	class Meta:
		model = Post
		fields = ['title','image', 'user','country','guide']
		widgets = { 'guide' : forms.Textarea(attrs = {'rows':12 , 'style':'resize:none'})}

##-----------------------------
User = get_user_model()

class UserLoginForm(forms.Form):
	username = forms.CharField(max_length = 254, widget=forms.TextInput(attrs={'class':"input-sm"}))
	password = forms.CharField(widget = forms.PasswordInput)

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get('password')
		if username and password:
			user = authenticate(username=username, password=password)
			if not user:
				raise forms.ValidationError("Incorrect password or User! Please try again.")

			if not user.check_password(password):
				raise forms.ValidationError("Incorrect password! Please try again.")

			if not user.is_active:
				raise forms.ValidationError("This user is no longer active!")
		return super(UserLoginForm, self).clean(*args, **kwargs)

#--------------------------------
class UserRegisterForm(forms.ModelForm):
	email = forms.EmailField(label = 'Email Address')
	password = forms.CharField(widget = forms.PasswordInput)
	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'password'
		]

	def clean_email(self):
		email = self.cleaned_data.get('email')
		email_qs = User.objects.filter(email=email)
		if email_qs.exists():
			raise forms.ValidationError("This email has already been registered!")
		return email

	def clean_username(self):
		username = self.cleaned_data.get('username')
		username_qs = User.objects.filter(username=username)
		if username_qs.exists():
			raise forms.ValidationError("This username has already been registered!")
		return username