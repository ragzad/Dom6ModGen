from django.db import models
from django.conf import settings # To link to the User model

class Nation(models.Model):
    # Consider adding ERA choices later (e.g., EA, MA, LA)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    # Link to the user who created/owns this nation concept
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, # Keep nation even if user deleted? Or CASCADE?
        null=True,
        blank=True, # Allow nations not tied to a specific user initially?
        related_name='created_nations'
    )
    generation_status = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']