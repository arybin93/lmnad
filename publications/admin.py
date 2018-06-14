from django.contrib import admin

from publications.models import Publication, Author, Journal

admin.site.register(Publication)
admin.site.register(Author)
admin.site.register(Journal)
