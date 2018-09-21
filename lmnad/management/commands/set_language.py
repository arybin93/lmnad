from django.core.management.base import BaseCommand
from lmnad.utils import detect_language_text
from publications.models import Publication, RU, EN


class Command(BaseCommand):
    help = 'Detect and set language for publication'

    def handle(self, *args, **options):
        publications = Publication.objects.all()

        for publication in publications:
            language = detect_language_text(publication.title_ru[:30])
            self.stdout.write(publication.title_ru[:30])
            self.stdout.write(language)
            if language == RU:
                publication.language = RU
            else:
                publication.language = EN

            publication.save()

        self.stdout.write('Done')
