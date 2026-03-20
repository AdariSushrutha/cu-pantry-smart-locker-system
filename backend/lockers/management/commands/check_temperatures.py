from django.core.management.base import BaseCommand
from lockers.utils import check_temperature_violations


class Command(BaseCommand):
    help = 'Check locker temperatures for food safety violations'

    def handle(self, *args, **kwargs):
        self.stdout.write('Checking locker temperatures...')

        violated_orders = check_temperature_violations()

        if not violated_orders:
            self.stdout.write(
                self.style.SUCCESS('No temperature violations found.')
            )
        else:
            for violation in violated_orders:
                self.stdout.write(
                    self.style.ERROR(
                        f'VIOLATION: Order #{violation["order_id"]} - '
                        f'Locker {violation["locker_number"]} - '
                        f'Student: {violation["student"]} - '
                        f'Temperatures: {violation["temperature_readings"]}'
                    )
                )

        self.stdout.write(f'Check complete. {len(violated_orders)} violation(s) found.')