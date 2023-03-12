from django import forms
from .models import ConversationMessage


class ConversationMessageForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))

    class Meta:
        model = ConversationMessage
        fields = ['content']