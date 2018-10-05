# -*- coding: utf-8 -*-
from django.forms import ModelForm, inlineformset_factory

from publications.models import Publication, Conference


class PublicationForm(ModelForm):
    class Meta:
        model = Publication
        fields = [
            'type',
            'title',
            'authors',
            'journal',
            'date',
            'pages',
            'is_rinc',
            'language'
        ]


class ConferenceForm(ModelForm):
    class Meta:
        model = Conference
        fields = ['form', 'author']


PublicationConferenceFormSet = inlineformset_factory(Publication, Conference, form=ConferenceForm, extra=1)
