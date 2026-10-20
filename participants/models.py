from django.db import models
from django.core.validators import MinLengthValidator
from django.utils.text import slugify

class Department(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        validators=[MinLengthValidator(2)],
        help_text='Name of the company department.',
    )
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField(
        blank=True,
        null=True,
        help_text='Optional summary of the department.',
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Participant(models.Model):
    first_name = models.CharField(
        max_length=30,
        validators=[MinLengthValidator(2)],
    )
    last_name = models.CharField(
        max_length=30,
        validators=[MinLengthValidator(2)],
    )
    slug = models.SlugField(unique=True, blank=True, null=True)
    email = models.EmailField(
        unique=True,
        help_text='Official company email address.',
    )
    profile_image_url = models.URLField(
        blank=True,
        null=True,
        help_text='Link to profile avatar image.',
    )

    # ForeignKey (One-To-Many relationship) linking employee to a single Department.
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='participants',
        help_text='Select the department this employee belongs to.',
    )
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['first_name', 'last_name']
        verbose_name = 'Participant'
        verbose_name_plural = 'Participants'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @staticmethod
    def get_top_performers(limit=5):
        """Returns top participants based on total logged workout distance."""
        return Participant.objects.annotate(
            total_km=models.Sum('activities__distance_km')
        ).order_by('-total_km')[:limit]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.first_name} {self.last_name}")
            self.slug = base_slug

        super().save(*args, **kwargs)

        expected_slug = slugify(f"{self.first_name} {self.last_name} {self.pk}")
        if self.slug != expected_slug:
            self.slug = expected_slug
            super().save(update_fields=['slug'])

    def __str__(self):
        return self.full_name

