from .models import Comment
from django import forms



class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Type your comment',
        'id': 'usercomment',
        'rows': '3'
    }))
    class Meta:
        model = Comment
        fields = ('content', )