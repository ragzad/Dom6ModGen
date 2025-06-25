import json
from django.core.management.base import BaseCommand
from gamedata.models import GameEntity

class Command(BaseCommand):
    help = 'Loads Dominions 6 game data from a JSONL file into the database.'

    def add_arguments(self, parser):
        parser.add_argument('jsonl_file', type=str, help='The path to the JSONL file to load.')

    def handle(self, *args, **options):
        file_path = options['jsonl_file']
        self.stdout.write(f"Loading data from {file_path}...")

        created_count = 0
        updated_count = 0

        with open(file_path, 'r') as f:
            for line in f:
                try:
                    data = json.loads(line)
                    
                    # Extract the core fields
                    entity_type = data.get('entity')
                    entity_id = data.get('entity_id')
                    attributes = data.get('attributes', {})
                    name = attributes.get('name', f"Unnamed {entity_type} {entity_id}")

                    if not all([entity_type, entity_id, name]):
                        self.stderr.write(self.style.WARNING(f"Skipping malformed line: {line.strip()}"))
                        continue

                    # Create or update the GameEntity object
                    obj, created = GameEntity.objects.update_or_create(
                        entity_type=entity_type,
                        entity_id=entity_id,
                        defaults={
                            'name': name,
                            'attributes': attributes,
                        }
                    )
                    
                    if created:
                        created_count += 1
                    else:
                        updated_count += 1

                except json.JSONDecodeError:
                    self.stderr.write(self.style.WARNING(f"Could not decode JSON from line: {line.strip()}"))
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f"Error processing line: {line.strip()}\n{e}"))

        self.stdout.write(self.style.SUCCESS(
            f'Successfully loaded data. Created: {created_count}, Updated: {updated_count}.'
        ))
