from django.db import models
from nations.models import Nation # Import Nation model

class Unit(models.Model):
    nation = models.ForeignKey(
        Nation,
        on_delete=models.CASCADE, # If nation is deleted, delete its units
        related_name='units'
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    # Placeholder for stats - will likely become more complex (ForeignKey to a Stats model, JSONField, etc.)
    stats_text = models.TextField(blank=True, null=True, help_text="Temporary: Enter stats as text")
    sprite_url = models.URLField(blank=True, null=True, help_text="URL to the generated or uploaded sprite")
    # Add fields for cost, resources, upkeep, slots, etc. later
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.nation.name})"

    class Meta:
        ordering = ['nation', 'name']
        # Ensure unit names are unique within a nation
        unique_together = ('nation', 'name')