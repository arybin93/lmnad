from django.core.management.base import BaseCommand, CommandError
from igwatlas.models import *
import sqlite3
from geoposition import Geoposition


class Command(BaseCommand):
    help = 'Import Data base from SQLite DB'

    def handle(self, *args, **options):
        conn = None
        try:
            # save data to db
            is_save = True

            conn = sqlite3.connect('igwdata.db')
            conn.text_factory = str
            cursor = conn.execute("SELECT * FROM records;")

            for row in cursor:
                id = row[0]
                lon = row[1]
                lat = row[2]
                date = row[3]
                types = row[4]
                file_name_source = row[5]
                pages = row[6]
                file_name_img = row[7]

                if not all([id, lon, lat, types, file_name_source, pages, file_name_img]):
                    continue

                # parse types
                record_types = []
                types_list = types.split(',')
                for el_type in types_list:
                    if el_type == 'M':
                        record_types.append(Record.MAP)
                    elif el_type == 'G':
                        record_types.append(Record.GRAPHIC)
                    elif el_type == 'S':
                        record_types.append(Record.SATELLITE)
                    elif el_type == 'R':
                        record_types.append(Record.RECORD)
                    elif el_type == 'T':
                        record_types.append(Record.TABLE)

                if is_save:
                    # save file
                    try:
                        file_source = File.objects.get(path=file_name_source)
                    except File.DoesNotExist:
                        file_source = File.objects.create(path=file_name_source,
                                                          file=file_name_source)
                    else:
                        file_source.path = file_name_source
                        file_source.file = 'uploads/igwatlas/sources/' + file_name_source
                        file_source.save()
                    # save record
                    try:
                        record = Record.objects.get(id=id)
                    except Record.DoesNotExist:
                        record = Record.objects.create(id=id,
                                                       position=Geoposition(lat, lon),
                                                       types=str(record_types),
                                                       page=pages,
                                                       image=file_name_img,
                                                       file=file_source
                                                       )
                    else:
                        record.position = Geoposition(lat, lon)
                        record.types = str(record_types)
                        record.page = pages
                        file_name_img = file_name_img.replace("tiff", "jpg")
                        record.image = 'uploads/igwatlas/images/' + file_name_img
                        record.file = file_source
                        record.save()

                    # get source
                    query = "SELECT * FROM relation INNER JOIN sources on SourceID=id where recID={};".format(id)
                    cursor_source = conn.execute(query)

                    for row_source in cursor_source:
                        id_source = row_source[2]
                        source_text = row_source[3]
                        source_short_text = row_source[4]

                        # save source
                        try:
                            source = Source.objects.get(id=id_source)
                        except Source.DoesNotExist:
                            source = Source.objects.create(id=id_source,
                                                           source=source_text,
                                                           source_short=source_short_text)
                        else:
                            source.source = source_text
                            source.source_short = source_short_text
                            source.save()

                        if source not in record.source.all():
                            record.source.add(source)

                        record.save()
            self.stdout.write(self.style.SUCCESS('Successfully import db'))
        except sqlite3.Error as e:
            if conn:
                conn.close()
        finally:
            if conn:
                conn.close()

