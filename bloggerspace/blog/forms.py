from django import forms
from .models import Comment, Post, Tag

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ["post"]
        labels = {
            "user_name": "Your name",
            "user_email": "Your email",
            "text": "Your comment"
        }

choices = Tag.objects.all().values_list('caption', 'caption')

choice_list = []

for item in choices:
    choice_list.append(item)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'excerpt', 'image', 'author','content', 'tags')

        # widgets = {
        #     'title': forms.TextInput(attrs={'class':'form-control'}),
        #     'excerpt': forms.TextInput(attrs={'class':'form-control'}),
        #     'image': forms.ImageField(attrs={'class':'form-control'}),
        #     'author': forms.Select(attrs={'class':'form-control'}),
        #     'content': forms.Textarea(attrs={'class':'form-control'}),
        #     'tags': forms.Select(choices=choice_list, attrs={'class':'form-control'}),
        # }

