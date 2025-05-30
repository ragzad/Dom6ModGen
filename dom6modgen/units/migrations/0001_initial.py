# Generated by Django 5.2 on 2025-04-23 20:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('nations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('stats_text', models.TextField(blank=True, help_text='Temporary: Enter stats as text', null=True)),
                ('sprite_url', models.URLField(blank=True, help_text='URL to the generated or uploaded sprite', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('nation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='units', to='nations.nation')),
            ],
            options={
                'ordering': ['nation', 'name'],
                'unique_together': {('nation', 'name')},
            },
        ),
    ]
