# dom6modgen/gamedata/models.py
from django.db import models
import json

class GameEntity(models.Model):
    """
    A flexible model to store any entity from the Dominions 6 data.
    """
    ENTITY_CHOICES = [
        ('MagicSites', 'Magic Site'), ('Mercenary', 'Mercenary'), ('afflictions', 'Affliction'),
        ('anon_province_events', 'Anonymous Province Event'), ('armors', 'Armor'), ('attribute_keys', 'Attribute Key'),
        ('attributes_by_armor', 'Attributes by Armor'), ('attributes_by_nation', 'Attributes by Nation'),
        ('attributes_by_spell', 'Attributes by Spell'), ('attributes_by_weapon', 'Attributes by Weapon'),
        ('buffs_1_types', 'Buff Type 1'), ('buffs_2_types', 'Buff Type 2'),
        ('coast_leader_types_by_nation', 'Coast Leader'), ('coast_troop_types_by_nation', 'Coast Troop'),
        ('effect_modifier_bits', 'Effect Modifier Bit'), ('effects_info', 'Effect Info'),
        ('effects_spells', 'Effect Spell'), ('effects_weapons', 'Effect Weapon'),
        ('enchantments', 'Enchantment'), ('events', 'Event'), ('fort_leader_types_by_nation', 'Fort Leader'),
        ('fort_troop_types_by_nation', 'Fort Troop'), ('item', 'Item'), ('magic_paths', 'Magic Path'),
        ('map_terrain_types', 'Map Terrain Type'), ('monster_tags', 'Monster Tag'), ('nametypes', 'Name Type'),
        ('nations', 'Nation'), ('nonfort_leader_types_by_nation', 'Non-Fort Leader'),
        ('nonfort_troop_types_by_nation', 'Non-Fort Troop'), ('other_planes', 'Other Plane'),
        ('pretender_types_by_nation', 'Pretender Type'), ('protections_by_armor', 'Protections by Armor'),
        ('realms', 'Realm'), ('site_terrain_types', 'Site Terrain Type'),
        ('special_damage_types', 'Special Damage Type'), ('special_unique_summons', 'Special Unique Summon'),
        ('spell', 'Spell'), ('terrain_specific_summons', 'Terrain Specific Summon'),
        ('unit', 'Unit'), ('unit_effects', 'Unit Effect'),
        ('unpretender_types_by_nation', 'Unpretender Type'), ('weapons', 'Weapon'),
    ]

    entity_type = models.CharField(max_length=50, choices=ENTITY_CHOICES, db_index=True)
    entity_id = models.IntegerField(db_index=True, null=True, blank=True)
    name = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    attributes = models.JSONField(help_text="All other attributes from the JSONL file.")
    reference_text = models.TextField(help_text="Pre-formatted text for the AI prompt")

    class Meta:
        ordering = ['entity_type', 'name']

    def __str__(self):
        return f"{self.name or 'Unnamed'} ({self.entity_type} - ID: {self.entity_id or 'N/A'})"

    def save(self, *args, **kwargs):
        attr_str = json.dumps(self.attributes)
        self.reference_text = f"ID: {self.entity_id or 'N/A'}, Name: {self.name or 'Unnamed'}, Type: {self.entity_type}, Attributes: {attr_str}"
        super().save(*args, **kwargs)

class ModExample(models.Model):
    """
    Stores a complete, working .dm mod file to be used as a
    high-quality example in few-shot prompting.
    """
    name = models.CharField(max_length=100, unique=True, help_text="A descriptive name for the mod example.")
    mod_text = models.TextField(help_text="The full text content of the .dm file.")

    def __str__(self):
        return self.name
