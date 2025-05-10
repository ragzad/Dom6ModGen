from django.contrib import admin
from .models import Nation 

admin.site.register(Nation)
admin.site.register(ModGenerationJob) # Register the new model
