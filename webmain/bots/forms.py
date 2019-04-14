from django import forms
from .models import Bot

class BotForm(forms.ModelForm):
    class Meta:
        model = Bot
        fields = ['name']
    def save(self, game=None, commit=True):
        instance = super(BotForm, self).save(commit=False)
        if game != None:
            instance.game = game
        if commit:
            instance.save()
        return instance
            



