from django import forms
from .models import Badge, ActivityLog

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
        fields = ['participant', 'activity_type', 'distance_km', 'activity_date', 'notes']
        widgets = {
            'participant': forms.Select(attrs={'class': 'form-control'}),
            'activity_type': forms.Select(attrs={'class': 'form-control'}),
            'distance_km': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': '5.0'}),
            'activity_date':forms.DateInput(attrs={'class': 'form-control', 'type':'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Optional remarks...'}),
        }

class AwardBadgeForm(forms.Form):
    #UI Form to award an existing badge to a participant.
    badge = forms.ModelChoiceField(
        queryset=Badge.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Select Badge',
    )