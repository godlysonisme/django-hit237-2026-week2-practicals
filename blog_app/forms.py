from django import forms
from .models import Post 
 
class PostForm(forms.ModelForm):
    """
    Form for creating and updating blog posts.
    Handles validation at the form level before passing to model.
    """
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Post Title',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Post Content',
                'rows': 10,
            }),
        }