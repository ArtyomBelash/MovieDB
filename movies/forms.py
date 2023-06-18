from django import forms
from .models import Comment


# class CommentForm(forms.Form):
#     class Meta:
#         model = Comment
#         fields = ['body']


class CommentForm(forms.Form):
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'style': 'resize:none',
                'class': 'form-control',
                'placeholder': 'Коментарии могут оставлять только авторизованные пользователи'
            }
        )
    )