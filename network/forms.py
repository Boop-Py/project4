from django import forms

class Post_Form(forms.Form):
    content = forms.CharField(max_length=255)