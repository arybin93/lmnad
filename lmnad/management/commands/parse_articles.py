from django.core.management.base import BaseCommand, CommandError
from lmnad.models import Article
from publications.models import Publication, Author, AuthorPublication, Journal
import datetime
from django.utils.timezone import utc


class Command(BaseCommand):
    help = 'Parse old articles and create new publications'

    def handle(self, *args, **options):
        articles = Article.objects.all()

        for article in articles:
            # parse Journal, Volume
            journal_text = article.source.split(',')
            journal_name = journal_text[0]
            try:
                volume_pages = journal_text[1]
            except IndexError:
                volume_pages = ''

            try:
                journal = Journal.objects.get(name=journal_name)
            except Journal.DoesNotExist:
                journal = Journal.objects.create(name=journal_name)

            # parse Authors
            authors_list = article.authors.split(',')
            publication_authors = []
            for aut in authors_list:
                if len(aut) > 5:
                    aut = aut.strip()
                    try:
                        author = Author.objects.get(name=aut)
                    except Author.DoesNotExist:
                        author = Author.objects.create(name=aut,
                                                       last_name=aut,
                                                       middle_name=aut)
                    publication_authors.append(author)

            # create publication
            try:
                publication = Publication.objects.get(title=article.title)
            except Publication.DoesNotExist:
                publication = Publication.objects.create(title=article.title,
                                                         year=article.year,
                                                         date=article.date,
                                                         journal=journal,
                                                         volume=volume_pages,
                                                         pages=volume_pages)

            order = 0
            for author in publication_authors:
                try:
                    AuthorPublication.objects.get(author=author,
                                                  publication=publication)
                except AuthorPublication.DoesNotExist:
                    AuthorPublication.objects.create(author=author,
                                                     publication=publication,
                                                     order_by=order)
                    order += 1

        self.stdout.write('Done')
