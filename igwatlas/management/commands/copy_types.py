import re
from django.core.management.base import BaseCommand, CommandError
from igwatlas.models import RecordType, Record
import datetime
from django.utils.timezone import utc

MAP = 0
GRAPHIC = 1
SATELLITE = 2
RECORD = 3
TABLE = 4

TYPES = (
    (MAP, 'Карта'),
    (GRAPHIC, 'График'),
    (SATELLITE, 'Спутниковый снимок'),
    (RECORD, 'Запись'),
    (TABLE, 'Таблица')
)


def parse_types(types):
    reg_number = re.compile(r'(\d+)')
    types_list = []
    for r in reg_number.findall(types):
        types_list.append(r)

    return types_list


class Command(BaseCommand):
    help = 'Copy types'

    def handle(self, *args, **options):
        # create RecordType
        for item in TYPES:
            RecordType.objects.get_or_create(name=item[1], value=item[0])

        records = Record.objects.all()
        for rec in records:
            lst_types = parse_types(rec.types)
            print(lst_types)

            for tp_txt in lst_types:
                print(tp_txt)
                record_type = RecordType.objects.get(value=int(tp_txt))

                # save new types
                if record_type not in rec.new_types.all():
                    rec.new_types.add(record_type)

            rec.save()
