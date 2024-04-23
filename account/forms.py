from django import forms
from tinymce.widgets import TinyMCE
from .models import BlogPost

class BlogPostForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = BlogPost
        fields = ['title', 'heading','content', 'category', 'published_date', 'user', 'image']
        # Make sure to include all other fields you want to be part of the form
