from django.core.management.base import BaseCommand, CommandError
from lmnad.models import Article
from publications.models import Publication, Author, AuthorPublication, Journal
import datetime
from django.utils.timezone import utc


class Command(BaseCommand):
    help = 'Parse old articles and create new publications'

    def handle(self, *args, **options):
        articles = Article.objects.all()
