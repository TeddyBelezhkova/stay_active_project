from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

from participants.models import Participant


def validate_not_future_date(value):
    if value > timezone.now().date():
        raise ValidationError('Activity date cannot be in the future.')

# Model 1: Badge (Milestone achievement badge)
class Badge(models.Model):
    title = models.CharField(
        max_length=60,
        unique=True,
    )
    description = models.TextField(
        help_text='Requirements or criteria to earn this badge.',
    )
    badge_image_url = models.URLField(
        blank=True,
        null=True,
        help_text='Optional. Direct image URL for the badge.',
    )

    # Flexible textual requirement (e.g., "Log 10 Yoga Sessions", "Hit 100 KM")
    criteria = models.CharField(
        max_length=100,
        default='Complete challenge goal',
        help_text="e.g., 'Log 10 Yoga sessions', 'Run 50 KM', or 'Complete 5 workouts in a week'.",
    )

    # Many-to-Many Relationship:
    # A single badge can be awarded to multiple participants,
    # and a participant can collect multiple badges.
    participants = models.ManyToManyField(
        Participant,
        blank=True,
        related_name='badges',
        help_text='Participants who have earned this badge.',
    )

    class Meta:
        ordering = ['title']
        verbose_name = 'Badge'
        verbose_name_plural = 'Badges'

    def __str__(self):
        return self.title

# Model 2: ActivityLog (stores individual fitness submissions from participants)
class ActivityLog(models.Model):
    ACTIVITY_CHOICES = (
        ('Running', 'Running'),
        ('Walking', 'Walking'),
        ('Cycling', 'Cycling'),
        ('Hiking', 'Hiking'),
        ('Swimming', 'Swimming'),
        ('Yoga', 'Yoga & Pilates'),
        ('Strength', 'Strength Training'),
        ('Other', 'Other Activity'),
    )

    # Foreign Key (One-To-Many relationship):
    # One participant can have many activity logs.
    # Deleting a participant deletes all their activity entries.
    participant = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE,
        related_name='activities',
        help_text='Select the participant submitting kilometers or workout hours.',
    )

    # Selected category of physical activity
    activity_type = models.CharField(
        max_length=20,
        choices=ACTIVITY_CHOICES,
        default='Running',
    )

    # Measured effort value (e.g., distance in KM or duration in hours/units)
    distance_km = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[
            MinValueValidator(0.1, message='Value must be at least 0.1.'),
            MaxValueValidator(500.0, message='Single log entry cannot exceed 500.'),
        ],
        help_text='Enter distance in KM or workout metric equivalent (e.g. duration in hours/units)'
    )

    activity_date = models.DateField(
        validators=[validate_not_future_date],  #using custom validator
        help_text='Date when activity was performed.',
    )

    notes = models.TextField(
        blank=True,
        null=True,
        help_text='Optional remarks about the activity.',
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-activity_date', '-created_at']  # Newest entries shown first
        verbose_name = 'Activity Log'
        verbose_name_plural = 'Activity Logs'

    def __str__(self):
        return f"{self.participant.full_name} - {self.activity_type} ({self.distance_km})"






