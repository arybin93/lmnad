# -*- coding: utf-8 -*-
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.db.models import Q

from lmnad.models import *
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth import logout

from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
from constance import config

def home(request):
    home = Page.objects.get(name='home')
    context = {
        'home': home
    }
    return render(request, 'lmnad/home.html', context)


def people(request):
    peoples = People.objects.filter(status=True)
    peoples_old = People.objects.filter(status=False)
    context = {
        'peoples': peoples,
        'peoples_old': peoples_old,
    }
    return render(request, 'lmnad/people.html', context)


def articles(request):
    query = request.GET.get('query', None)
    page = request.GET.get('page', 1)

    if query:
        if isinstance(query, int):
            article_list = Article.objects.filter(year=query)
        else:
            article_list = Article.objects.filter(Q(title__icontains=query) | Q(authors__icontains=query) |
                                                  Q(abstract__icontains=query))
    else:
        article_list = Article.objects.all()

    paginator = Paginator(article_list, 15)

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

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

def seminar_detail(request, pk):
    seminar = Seminar.objects.get(pk=pk)

    context = {
        'seminar': seminar
    }
    return render(request, 'lmnad/seminars_details.html', context)


def protections(request):
    protections = Protection.objects.all()
    context = {
        'protections': protections
    }
    return render(request, 'lmnad/protections.html', context)


def grants(request):
    grants = Grant.objects.all()

    context = {
        'grants': grants
    }
    return render(request, 'lmnad/grants.html', context)


def grants_detail(request, number):
    grant = Grant.objects.get(number=number)

    context = {
        'grant': grant
    }
    return render(request, 'lmnad/grants_detail.html', context)

def projects(request):
    projects = Project.objects.all()
    context = {
        'projects': projects
    }
    return render(request, 'lmnad/projects.html', context)


def project_detail(request, name):
    project = Project.objects.get(name=name)

    context = {
        'project': project
    }
    return render(request, 'lmnad/project_details.html', context)


def events(request):
    events = Event.objects.all()
    context = {
        'events': events
    }
    return render(request, 'lmnad/events.html', context)


def event_detail(request, pk):
    event = Event.objects.get(pk=pk)

    context = {
        'event': event
    }
    return render(request, 'lmnad/events_details.html', context)


def contacts(request):
    contacts = Page.objects.get(name='contacts')
    context = {
        'contacts': contacts
    }
    return render(request, 'lmnad/contacts.html', context)


def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        ## 404
        pass
    else:
        context = {
            'profile': user
        }
        return render(request, 'lmnad/profile.html', context)


class EditProfileForm(forms.Form):
    email = forms.EmailField(label='email', max_length=200, required=False,
                             widget=forms.TextInput(attrs = {'class': 'form-control'}))
    is_subscribe = forms.BooleanField(label=u'Подписка на рассылку', required=False)
    text = forms.CharField(widget=CKEditorUploadingWidget(), required=False, label=u'Текст страницы')
    cv_file = forms.FileField(required=False, label=u'CV файл')


def EditProfileView(request):
    current_user = request.user
    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            is_subscribe = form.cleaned_data['is_subscribe']
            text = form.cleaned_data['text']
            cv_file = form.cleaned_data['cv_file']

            current_user.email = email
            try:
                account = Account.objects.get(user_id=current_user.id)
            except Account.DoesNotExist:
                account = Account.objects.create(is_subscribe=is_subscribe,
                                                 text=text,
                                                 cv_file=cv_file,
                                                 user_id=current_user.id)
            else:
                current_user.account.is_subscribe = is_subscribe
                current_user.account.text = text
                current_user.account.cv_file = cv_file
                current_user.account.save()

            current_user.save()

            context = {
                'profile': current_user
            }

            return render(request, 'lmnad/profile.html', context)
    else:
        try:
            current_user.account
        except Account.DoesNotExist:
            init = {}
        else:
            is_subscribe = current_user.account.is_subscribe
            text = current_user.account.text
            cv_file = current_user.account.cv_file
            init = {"email": current_user.email,
                    "is_subscribe": is_subscribe,
                    "text": text,
                    "cv_file": cv_file}

        form = EditProfileForm(initial=init)

    context = {
        'form': form
    }

    return render(request, 'lmnad/edit_profile.html', context)


def logoutView(request):
    logout(request)
    return redirect('home')


class RegisterFormView(FormView):
    form_class = UserCreationForm

    success_url = "/login/"

    template_name = "lmnad/register.html"

    def form_valid(self, form):
        form.save()

        return super(RegisterFormView, self).form_valid(form)


class LoginFormView(FormView):
    form_class = AuthenticationForm

    template_name = "lmnad/login.html"

    success_url = "/"

    def form_valid(self, form):
        self.user = form.get_user()

        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100, label=u'Тема:',
                              widget = forms.TextInput(attrs = {'class': 'form-control'}))
    sender = forms.EmailField(label=u'Отправитель:',
                              widget = forms.TextInput(attrs = {'class': 'form-control'}))
    message = forms.CharField(label=u'Текст:',
                              widget=forms.Textarea(attrs={'class': 'form-control'}))
    copy = forms.BooleanField(required=False, label=u'Отправить копию себе:')


def contactView(request):
    contacts = Page.objects.get(name='contacts')

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            sender = form.cleaned_data['sender']
            message = form.cleaned_data['message']
            copy = form.cleaned_data['copy']

            recipient_list = config.FEEDBACK_EMAIL.split(',')
            if copy:
                recipient_list.append(sender)
            try:
                send_mail(subject, message, 'lmnad@nntu.ru', recipient_list)
            except BadHeaderError:
                return HttpResponse('Invalid header found')
            return render(request, 'lmnad/thanks.html')
    else:
        form = ContactForm()

    context = {
        'contacts': contacts,
        'form': form
    }

    return render(request, 'lmnad/contacts.html', context)
