from django import forms
from django.contrib. auth.forms import UserCreationForm
from django.contrib.auth.models import User
from blog.models import Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'text']
class SignupForm(UserCreationForm):
    first_name =forms. CharField(max_length=32, required=True)
    last_name =forms.CharField(max_length=32, required=True)
    email =forms.EmailField(max_length=256,required=True)
    bio = forms.CharField(max_length=300, widget=forms.Textarea)

    class Meta:
        model = User
        fields = ('username','first_name','last_name','bio','email', 'password1','password2')
        
class LoginForm(UserCreationForm):
    username=forms. CharField(max_length=32, required=True)
    password = forms.CharField(widget = forms.PasswordInput())
