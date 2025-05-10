from django.contrib import admin
from .models import Nation, ModGenerationJob

admin.site.register(Nation)
admin.site.register(ModGenerationJob) # Register the new model
