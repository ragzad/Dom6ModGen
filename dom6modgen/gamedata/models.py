# dom6modgen/gamedata/models.py
from django.db import models
import json

class GameEntity(models.Model):
    """
    A flexible model to store any entity from the Dominions 6 data,
    designed to be populated from a JSONL file.
    """
    ENTITY_CHOICES = [
        ('unit', 'Unit'),
        ('weapon', 'Weapon'),
        ('armor', 'Armor'),
        ('spell', 'Spell'),
        ('site', 'Magic Site'),
        # Add other entity types from your file here
    ]

    # Core identifying information, indexed for fast lookups
    entity_type = models.CharField(max_length=20, choices=ENTITY_CHOICES, db_index=True)
    entity_id = models.IntegerField(db_index=True)
    name = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    
    # Store all other attributes from the JSONL file in a single JSON field.
    # This is highly flexible and avoids needing dozens of columns.
    attributes = models.JSONField(help_text="All other attributes from the JSONL file.")

    # We will pre-format the text for prompt injection to make lookups faster later.
    reference_text = models.TextField(help_text="Pre-formatted text for the AI prompt")

    class Meta:
        # This ensures you can't have two units with the same ID, but a unit and
        # a weapon can share an ID.
        unique_together = ('entity_type', 'entity_id')
        ordering = ['entity_type', 'name']

    def __str__(self):
        return f"{self.name} ({self.entity_type} - ID: {self.entity_id})"

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to automatically generate the
        reference_text field. This is an optimization so we don't have to
        format the text every time we generate a prompt.
        """
        # Create a clean, readable string of the key attributes for the AI.
        # We can customize this to be more or less verbose.
        attr_str = json.dumps(self.attributes)
        self.reference_text = f"ID: {self.entity_id}, Name: {self.name}, Attributes: {attr_str}"
        super().save(*args, **kwargs)
