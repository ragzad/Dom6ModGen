from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse # Make sure to import reverse

# The different stages of the mod generation process
GENERATION_STATUS_CHOICES = [
    ('not_started', 'Not Started'),
    ('prompt_expansion', 'Step 1: Expanding Prompt'),
    ('nation_details', 'Step 2: Nation Details'),
    ('commanders', 'Step 3: Commanders'),
    ('troops', 'Step 4: Troops'),
    ('weapons', 'Step 5: Weapons'),
    ('armor', 'Step 6: Armor'),
    ('spells', 'Step 7: Spells'),
    ('completed', 'Completed'),
    ('failed', 'Failed'),
]


class Nation(models.Model):
    """
    Represents a moddable nation in Dominions 6.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(help_text="A brief, high-level description or idea for the nation.")
    
    expanded_description = models.TextField(
        blank=True,
        null=True,
        help_text="The AI-expanded, detailed design document for the nation."
    )

    generated_mod_code = models.TextField(
        blank=True,
        null=True,
        help_text="The accumulating .dm mod code generated at each step."
    )

    generation_status = models.CharField(
        max_length=20,
        choices=GENERATION_STATUS_CHOICES,
        default='not_started',
        help_text="The current stage of the mod generation process."
    )
    
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    # --- ADD THIS METHOD ---
    def get_absolute_url(self):
        """Returns the canonical URL for a nation instance."""
        return reverse('nations:nation_detail', kwargs={'pk': self.pk})