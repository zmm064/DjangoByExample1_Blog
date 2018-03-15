from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
    '''邮件发送表单，这里暂时不需要将发送情况保存到数据库中'''
    name     = forms.CharField(max_length=25)
    email    = forms.EmailField()
    to       = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')