# models.py
from django.db import models
from django.conf import settings # To link to the User model
from django.utils.translation import gettext_lazy as _ # For choices

# Added: Choices for tracking the generation task status
class NationGenerationStatus(models.TextChoices):
    PENDING = 'PENDING', _('Pending')
    GENERATING = 'GENERATING', _('Generating')
    SUCCESS = 'SUCCESS', _('Success')
    FAILURE = 'FAILURE', _('Failure')
    NONE = 'NONE', _('None') # Default state, before any generation attempt


class Nation(models.Model):
    # Consider adding ERA choices later (e.g., EA, MA, LA)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True) # Keep allowing blank descriptions
    # Link to the user who created/owns this nation concept
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, # Keep nation even if user deleted? Or CASCADE?
        null=True,
        blank=True, # Allow nations not tied to a specific user initially
        related_name='created_nations'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # --- Added fields for asynchronous generation tracking ---
    generation_status = models.CharField(
        max_length=15,
        choices=NationGenerationStatus.choices,
        default=NationGenerationStatus.NONE,
        help_text="Status of the last DM code generation task."
    )
    generated_dm_code = models.TextField(
        blank=True,
        null=True,
        help_text="The generated Dominions 6 mod code."
    )
    generation_error = models.TextField(
        blank=True,
        null=True,
        help_text="Error message if the last generation failed."
    )
    generation_task_id = models.CharField(
        max_length=50, # Celery task IDs are usually UUIDs (36 chars) but give some buffer
        blank=True,
        null=True,
        editable=False, # Should not be edited directly in admin/forms
        help_text="Celery Task ID for the last generation attempt."
    )
    # --- End of added fields ---

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']