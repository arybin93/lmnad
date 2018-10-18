from django.core.management.base import BaseCommand, CommandError
from igwatlas.models import *
import datetime
from django.utils.timezone import utc

class Command(BaseCommand):
    help = 'Import Dates from file to database'

    def handle(self, *args, **options):
        with open("records_with_dates.txt", "r") as ins:
            array = []
            for line in ins:
                array.append(line)

        for string in array:
            result = string.split('    ')
            id = result[0]
            date = result[3].strip('\n')

            try:
                record = Record.objects.get(pk=id)
            except Record.DoesNotExist:
                print('DoesNotExist')
            else:
                date = datetime.datetime.strptime(date, "%m/%d/%Y")
                date = date.replace(hour=0, minute=0, second=0)
                date = date.replace(tzinfo=utc)
                record.date = date
                record.save()
