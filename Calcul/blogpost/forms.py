from django import forms
from .models import *


class ConversationMessageForm(forms.ModelForm):
    content = forms.CharField(required=True, widget=forms.widgets.Textarea(
        attrs={'placeholder': 'Enter your Post', 'class': 'form-control'}), label='')

    class Meta:
        model = BlogPost
        fields = ['content']
        