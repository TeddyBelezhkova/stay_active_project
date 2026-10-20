from django import forms
from .models import Badge, ActivityLog, ActivityComment

class BadgeForm(forms.ModelForm):
    class Meta:
        model = Badge
        fields = ['title', 'description', 'badge_image_url', 'criteria']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 100 KM Club'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Badge criteria...'}),
            'badge_image_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'criteria': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Log 10 Yoga sessions'}),
        }

class ActivityLogForm(forms.ModelForm):
    class Meta:
        model = ActivityLog
        fields = [
            'participant',
            'activity_type',
            'distance_km',
            'activity_date',
            'notes',
            'proof_photo',
            'is_private',
        ]
        widgets = {
            'participant': forms.Select(attrs={'class': 'form-control'}),
            'activity_type': forms.Select(attrs={'class': 'form-control'}),
            'distance_km': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': '5.0'}),
            'activity_date':forms.DateInput(attrs={'class': 'form-control', 'type':'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Optional remarks...'}),
            'proof_photo': forms.FileInput(attrs={'class': 'form-control'}),
            'is_private': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
             }

class CommentForm(forms.ModelForm):
    class Meta:
        model = ActivityComment
        fields = ['author_name', 'content']
        widgets = {
            'author_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Add a comment...'}),
        }

class AwardBadgeForm(forms.Form):
    #UI Form to award an existing badge to a participant.
    badge = forms.ModelChoiceField(
        queryset=Badge.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Select Badge',
    )