from django import forms
from .models import *





class CommentForms(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['post']
        labels = {
            "user_name":"Your Name",
            "user_email":"Your Email",
            "text":"Your Comment"
        }
















