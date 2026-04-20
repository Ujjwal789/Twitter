from django import forms
from .models import tweet

class TweetForm(forms.ModelForm):
    class Meta:
        model = tweet
        fields = ['content', 'photo']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': "What's happening?"}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }