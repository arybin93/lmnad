from django.shortcuts import render
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response
from lmnad.serializers import *
from django.http import HttpResponse
from lmnad.models import *

def home(request):
    home = Page.objects.get(name='home')
    context = {
        'home': home
    }
    return render(request, 'lmnad/home.html', context)

def people(request):
    peoples = People.objects.all()
    context = {
        'peoples': peoples
    }
    return render(request, 'lmnad/people.html', context)

def articles(request):
    articles = Article.objects.all()
    context = {
        'articles': articles
    }
    return render(request, 'lmnad/articles.html', context)

def seminars(request):
    seminars = Seminar.objects.all()
    context = {
        'seminars': seminars
    }
    return render(request, 'lmnad/seminars.html', context)

def protections(request):
    protections = Protection.objects.all()
    context = {
        'protections': protections
    }
    return render(request, 'lmnad/protections.html', context)

def igwresearch(request):
    igwresearch = Page.objects.get(name='igwresearch')
    context = {
        'igwresearch': igwresearch
    }
    return render(request, 'lmnad/igwresearch.html', context)

def events(request):
    events = Event.objects.all()
    context = {
        'events': events
    }
    return render(request, 'lmnad/events.html', context)

def contacts(request):
    contacts = Page.objects.get(name='contacts')
    context = {
        'contacts': contacts
    }
    return render(request, 'lmnad/contacts.html', context)