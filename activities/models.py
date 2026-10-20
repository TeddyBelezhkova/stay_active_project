from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from participants.models import Participant
from activities.validators import FileSizeValidator


def validate_not_future_date(value):
    if value > timezone.now().date():
        raise ValidationError('Activity date cannot be in the future.')

# Model 1: Badge (Milestone achievement badge)
class Badge(models.Model):
    title = models.CharField(
        max_length=60,
        unique=True,
    )
    slug = models.SlugField(unique=True, blank=True, null=True)
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
        max_length=255,
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

    @staticmethod
    def get_default_badge_icon(activity_type):
        # Returns relative static fallback path based on activity category.
        icons = {
            'running': 'images/badges/runner.png',
            'cycling': 'images/badges/bike.png',
            'swimming': 'images/badges/swimmer.png',
        }
        return icons.get(activity_type, 'images/badges/default.png')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

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

    proof_photo = models.ImageField(
        upload_to='proof_photos/',
        blank=True,
        null=True,
        validators=[FileSizeValidator(max_mb=5)],
        help_text="Upload a photo as proof of achievement (max 5 MB)."
    )

    is_private = models.BooleanField(
        default=False,
        verbose_name='Hide photo from public Fame Board',
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
        return f"{self.participant.full_name} – {self.get_activity_type_display()} ({self.activity_date})"



class ActivityComment(models.Model):
    activity = models.ForeignKey(
        ActivityLog,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author_name = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Activity Comment'
        verbose_name_plural = 'Activity Comments'

    def __str__(self):
        return f"Comment by {self.author_name} on {self.activity}"

class ActivityReaction(models.Model):
    REACTION_CHOICES = [
        ('like', '👍 Like'),
        ('fire', '🔥 Fire'),
        ('clap', '👏 Clap'),
        ('trophy', '🏆 Trophy'),
    ]

    activity = models.ForeignKey(
        ActivityLog,
        on_delete=models.CASCADE,
        related_name='reactions',
    )
    reaction_type = models.CharField(max_length=20, choices=REACTION_CHOICES)
    user_identifier = models.CharField(max_length=100, default='anonymous')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('activity', 'reaction_type', 'user_identifier')
        verbose_name = 'Activity Reaction'
        verbose_name_plural = 'Activity Reactions'

    def __str__(self):
        return f"{self.get_reaction_type_display()} by {self.user_identifier} on {self.activity}"


