from django import forms
from django.contrib.auth.models import User
from basicapp.models import UserProfileInfoModel, Post, Comment

class ProfileInfoForm(forms.ModelForm):

    class Meta():
        model = UserProfileInfoModel
        fields = ('userportfoliosite','profile_pic')

class UserProfileInfoForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username','password','email')

class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ('title','text')

        widgets = {

            'title': forms.TextInput(attrs={'class':'textinputclass'}),
            'text': forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})
        }

class CommentForm(forms.ModelForm):
    class Meta():
        model = Comment
        fields = ('author','email','text')

        widgets = {
            'author': forms.TextInput(attrs={'class':'textinputclass'}),
            'email': forms.EmailInput(attrs={'class':'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'})
        }
