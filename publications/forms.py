# -*- coding: utf-8 -*-
from django.forms import ModelForm, inlineformset_factory, formset_factory, modelformset_factory
from django_select2.forms import Select2Widget, ModelSelect2Widget, ModelSelect2MultipleWidget
from formsetfield.fields import FormSetField

from publications.models import Publication, Conference, Author, Journal, AuthorPublication


class AuthorInlineForm(ModelForm):
    class Meta:
        model = AuthorPublication
        fields = ['order_by', 'author']
        widgets = {
            'author': ModelSelect2Widget(model=Author,
                                         search_fields=['last_name__icontains'],
                                         attrs={'class': 'form-control'})
        }

AuthorFormSet = formset_factory(AuthorInlineForm, extra=5, max_num=5, can_delete=True)


class ConferenceInlineForm(ModelForm):
    class Meta:
        model = Conference
        fields = ['form', 'author']
        widgets = {
            'author': ModelSelect2Widget(model=Author, search_fields=['last_name__icontains'])
        }

ConferenceAuthorFormSet = formset_factory(ConferenceInlineForm, extra=1, can_delete=True)


class PublicationForm(ModelForm):
    authors_order = FormSetField(formset_class=AuthorFormSet,
                           label=u'Авторы:',
                           template='publications/formsetfield.html')
    conference_author = FormSetField(formset_class=ConferenceAuthorFormSet,
                                     label=u'Участие в конференции:',
                                     template='publications/formsetfield.html')

    class Meta:
        model = Publication
        fields = [
            'type',
            'title',
            'journal',
            'year',
            'date',
            'volume',
            'issue',
            'pages',
            'number',
            'link',
            'doi',
            'is_rinc',
            'is_vak',
            'is_wos',
            'is_scopus',
            'is_other_db',
            'is_show',
            'authors_order',
            'conference_author'
        ]

        widgets = {
            'journal': ModelSelect2Widget(model=Journal, search_fields=['name__icontains'])
        }

    class Media:
        js = ('publications/publications.js',)
