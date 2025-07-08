
from django import forms
#from django.forms import EmailField

from . models import Post
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from . models import Comment
from . models import Profile


class signUpForm(UserCreationForm):
    email= forms.EmailField(required=True)
    class Meta:
        model=User
        fields =('username','email','password1','password2')
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        #fields = ('title', 'content', 'image')
        exclude=('slug','author', 'published','updated','status')
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields=['body']
        widgets = {
            'body': forms.Textarea(attrs={'rows':3, 'placeholder':'Enter your comment...'})
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields= ['full_name' , 'phone', 'address','profile_image']
class UserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','email',]

class ContactForm(forms.Form):
    name= forms.CharField(max_length=100 , label='Your name')
    email= forms.EmailField(label='Your mail')
    subject = forms.CharField(max_length=150 , label='subject')
    message = forms.CharField(widget=forms.Textarea,label='Your message')