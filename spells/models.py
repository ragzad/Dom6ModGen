from django.db import models
from nations.models import Nation # Import Nation model - Assuming dependency

class Spell(models.Model):
    # If spells can be independent of nations, remove or make ForeignKey nullable
    nation = models.ForeignKey(
        Nation,
        on_delete=models.CASCADE,
        related_name='spells',
        # Consider null=True, blank=True if spells can be generic
        # null=True,
        # blank=True,
    )
    name = models.CharField(max_length=100, unique=True) # Unique spell name?
    description = models.TextField(blank=True, null=True)
    # Add fields for school, level, research, effect, fatigue cost, etc. later
    effect_text = models.TextField(blank=True, null=True, help_text="Temporary: Describe spell effect")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Handle case where nation might be optional if i change the ForeignKey
        # if self.nation:
        #     return f"{self.name} ({self.nation.name})"
        # return self.name
        # Simplified based on current required Nation ForeignKey:
         return f"{self.name} ({self.nation.name})"


    class Meta:
        ordering = ['name']