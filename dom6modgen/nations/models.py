# Dom6ModGen/dom6modgen/nations/models.py
from django.db import models
from django.contrib.auth.models import User # Optional: if you want to link jobs to users

class Nation(models.Model):
    """
    Represents a nation in the Dominions 6 game.
    This is the core entity around which mods will be generated.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(default="A nation of great warriors and mages.")

    def __str__(self):
        return self.name

class ModGenerationJob(models.Model):
    """
    Tracks the multi-step process of generating a mod for a nation.
    This model holds the plan, generated code snippets, and overall status.
    It's the backbone for the client-side orchestrated generation.
    """
    STATUS_CHOICES = [
        ('PENDING_PLAN', 'Pending Plan Generation'),
        ('PLANNING', 'Generating Plan'),
        ('PLAN_GENERATED', 'Plan Generated, Awaiting Components'),
        ('GENERATING_COMPONENTS', 'Generating Components'),
        ('COMPONENTS_GENERATED', 'All Components Generated'), # All components attempted, some might have failed
        ('COMPILING', 'Compiling Mod File'),
        ('COMPLETED', 'Completed Successfully'),
        ('COMPLETED_WITH_ERRORS', 'Completed with Some Errors'), # Compiled, but some components might be missing/faulty
        ('FAILED_PLANNING', 'Failed During Planning'),
        ('FAILED_COMPONENT', 'Failed During Component Generation'), # A component failed, user might retry or compile as-is
        ('FAILED_COMPILATION', 'Failed During Compilation'),
    ]

    nation = models.ForeignKey(Nation, on_delete=models.CASCADE, related_name='mod_jobs')
    # user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) # Optional: Link to a user

    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='PENDING_PLAN')
    
    # Stores the AI-generated plan from the first phase.
    # This plan dictates what components (nation block, units, commanders, etc.) need to be generated.
    # Example: { 
    #   "nation_meta": {"id": "nation_block", "component_type": "nation_meta", "name_hint": "...", "concept": "..."}, 
    #   "commanders": [{"id": "cmd1", "component_type": "commander", "name_hint": "...", "concept": "..."}, ...], 
    #   ... 
    # }
    plan_details = models.JSONField(null=True, blank=True) 
    
    # Stores the generated .dm code snippets for each component.
    generated_snippets = models.JSONField(default=dict, blank=True)

    # Tracks the status of each individual component for UI feedback.
    component_statuses = models.JSONField(default=dict, blank=True)
    
    final_mod_content = models.TextField(null=True, blank=True) # Stores the fully compiled .dm file content
    error_message = models.TextField(null=True, blank=True) # Aggregates any errors encountered
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Mod Job {self.id} for {self.nation.name} - {self.get_status_display()}"
