import os
from django.core.management.base import BaseCommand
from django.conf import settings
from gamedata.models import ModExample

class Command(BaseCommand):
    help = 'Loads *.dm mod files from a specified directory to use as examples.'

    def add_arguments(self, parser):
        """
        Adds a command-line argument for the directory containing the .dm files.
        """
        parser.add_argument('examples_dir', type=str, help='The path to the directory with .dm files, relative to the project base.')

    def handle(self, *args, **options):
        """
        The main logic of the command. It scans a directory, reads each .dm file,
        and saves its content to the ModExample model in the database.
        """
        # Build the full path to the directory
        relative_dir = options['examples_dir']
        full_dir_path = os.path.join(settings.BASE_DIR, relative_dir)

        if not os.path.isdir(full_dir_path):
            self.stderr.write(self.style.ERROR(f"Directory not found: {full_dir_path}"))
            return

        self.stdout.write(f"Scanning for .dm files in {full_dir_path}...")

        created_count = 0
        updated_count = 0

        # Loop through all files in the specified directory
        for filename in os.listdir(full_dir_path):
            if filename.endswith(".dm"):
                self.stdout.write(f"  - Found mod example: {filename}")
                file_path = os.path.join(full_dir_path, filename)
                
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        mod_text = f.read()

                    # Use the filename (without extension) as the unique name
                    mod_name = os.path.splitext(filename)[0]

                    # Create or update the ModExample object
                    obj, created = ModExample.objects.update_or_create(
                        name=mod_name,
                        defaults={'mod_text': mod_text}
                    )
                    
                    if created:
                        created_count += 1
                    else:
                        updated_count += 1

                except Exception as e:
                    self.stderr.write(self.style.ERROR(f"Error processing file {filename}: {e}"))

        self.stdout.write(self.style.SUCCESS(
            f'Successfully processed mod examples. Created: {created_count}, Updated: {updated_count}.'
        ))

