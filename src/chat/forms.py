from django.forms import ModelForm

from .models import ConversationMessage


class MessageForm(ModelForm):
    class Meta:
        model = ConversationMessage
        fields = ('body',)