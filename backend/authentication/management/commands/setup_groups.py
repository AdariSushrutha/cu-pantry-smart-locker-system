from django.core.management.base import BaseCommand
from authentication.groups import create_groups


class Command(BaseCommand):
    help = 'Create user role groups for the CU Pantry system'

    def handle(self, *args, **kwargs):
        self.stdout.write('Setting up user groups...')
        create_groups()
        self.stdout.write(self.style.SUCCESS('Successfully created all groups!'))