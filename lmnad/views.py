# -*- coding: utf-8 -*-
from django.contrib import messages
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.db.models import Q
from django.views.decorators.http import require_http_methods

from lmnad.models import *
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth import logout

from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
from constance import config

from publications.forms import PublicationForm
from publications.functions import export_from_profile
from publications.models import Publication, Conference
from datetime import datetime


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
        try:
            year = int(query)
            article_list = Article.objects.filter(year=year)
        except ValueError:
            article_list = Article.objects.filter(Q(title__icontains=query) | Q(authors__icontains=query) |
                                                  Q(abstract__icontains=query))
    else:
        article_list = Article.objects.all()

    article_list = article_list.order_by('-year')
    paginator = Paginator(article_list, 5)

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
    seminars_list = Seminar.objects.all().order_by('-date')
    page = request.GET.get('page', 1)

    paginator = Paginator(seminars_list, 5)
    try:
        seminars_page = paginator.page(page)
    except PageNotAnInteger:
        seminars_page = paginator.page(1)
    except EmptyPage:
        seminars_page = paginator.page(paginator.num_pages)

    context = {
        'seminars': seminars_page
    }

    return render(request, 'lmnad/seminars.html', context)


def seminar_detail(request, pk):
    seminar = Seminar.objects.get(pk=pk)

    context = {
        'seminar': seminar
    }
    return render(request, 'lmnad/seminars_details.html', context)


def protections(request):
    protections_list = Protection.objects.all().order_by('-date')
    page = request.GET.get('page', 1)

    paginator = Paginator(protections_list, 5)
    try:
        protections_page = paginator.page(page)
    except PageNotAnInteger:
        protections_page = paginator.page(1)
    except EmptyPage:
        protections_page = paginator.page(paginator.num_pages)

    context = {
        'protections': protections_page
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
    events_list = Event.objects.all().order_by('-date')
    page = request.GET.get('page', 1)

    paginator = Paginator(events_list, 5)
    try:
        events_page = paginator.page(page)
    except PageNotAnInteger:
        events_page = paginator.page(1)
    except EmptyPage:
        events_page = paginator.page(paginator.num_pages)

    context = {
        'events': events_page
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
    user = get_object_or_404(User, username=username)

    year_from = request.GET.get('year_from', None)
    year_to = request.GET.get('year_to', None)
    types = request.GET.getlist('type', [])
    enable_checkbox = request.GET.get('enable_checkbox', False)
    rinc = request.GET.get('rinc', False)
    vak = request.GET.get('vak', False)
    wos = request.GET.get('wos', False)
    scopus = request.GET.get('scopus', False)

    publications = Publication.objects.filter(authors__user=user.account, is_show=True).order_by('-year')

    if year_from and year_to:
        publications = publications.filter(year__gte=int(year_from), year__lte=int(year_to))
    elif year_to:
        publications = publications.filter(year__lte=int(year_to))
    elif year_from:
        publications = publications.filter(year__gte=int(year_from))

    if types:
        publications = publications.filter(type__in=types)

    if enable_checkbox == 'on':
        if rinc and rinc == 'on':
            is_rinc = True
        else:
            is_rinc = False

        if vak and vak == 'on':
            is_vak = True
        else:
            is_vak = False

        if wos and wos == 'on':
            is_wos = True
        else:
            is_wos = False

        if scopus and scopus == 'on':
            is_scopus = True
        else:
            is_scopus = False

        publications = publications.filter(Q(is_rinc=is_rinc) &
                                           Q(is_vak=is_vak) &
                                           Q(is_wos=is_wos) &
                                           Q(is_scopus=is_scopus))

    grants_member = Grant.objects.filter(members__account=user.account).order_by('-date_start')
    grants_head = Grant.objects.filter(head__account=user.account).order_by('-date_start')

    if year_from and year_to:
        grants_member = grants_member.filter(date_start__year__gte=int(year_from), date_end__year__lte=int(year_to))
        grants_head = grants_head.filter(date_start__year__gte=int(year_from), date_end__year__lte=int(year_to))
    elif year_to:
        grants_member = grants_member.filter(date_start__year__lte=int(year_to))
        grants_head = grants_head.filter(date_end__year__lte=int(year_to))
    elif year_from:
        grants_member = grants_member.filter(date_end__year__gte=int(year_from))
        grants_head = grants_head.filter(date_start__year__gte=int(year_from))

    grants_head_ids = grants_head.values('id')
    grants_member = grants_member.exclude(id__in=grants_head_ids)

    conferences = Conference.objects.filter(author__user=user.account)
    if year_from and year_to:
        conferences = conferences.filter(publication__journal__date_start__year__gte=int(year_from),
                                         publication__journal__date_stop__year__lte=int(year_to))
    elif year_to:
        conferences = conferences.filter(publication__journal__date_start__year__lte=int(year_to))
    elif year_from:
        conferences = conferences.filter(publication__journal__date_stop__year__lte=int(year_from))

    conferences = conferences.order_by('-publication__journal__date_start')

    stats = {
        'publication_count': publications.count(),
        'grants_member_count': grants_member.count(),
        'grants_head_count': grants_head.count(),
        'conferences': conferences.count(),
    }

    context = {
        'profile': user,
        'publications': publications,
        'grants_member': grants_member,
        'grants_head': grants_head,
        'conferences': conferences,
        'stats': stats,
    }
    return render(request, 'lmnad/profile.html', context)


def profile_export(request, username):
    user = get_object_or_404(User, username=username)

    year_from = request.GET.get('year_from', None)
    year_to = request.GET.get('year_to', None)
    types = request.GET.getlist('type', [])
    enable_checkbox = request.GET.get('enable_checkbox', False)
    rinc = request.GET.get('rinc', False)
    vak = request.GET.get('vak', False)
    wos = request.GET.get('wos', False)
    scopus = request.GET.get('scopus', False)

    publications = Publication.objects.filter(authors__user=user.account, is_show=True).order_by('-year')

    if year_from and year_to:
        publications = publications.filter(year__gte=int(year_from), year__lte=int(year_to))
    elif year_to:
        publications = publications.filter(year__lte=int(year_to))
    elif year_from:
        publications = publications.filter(year__gte=int(year_from))

    if types:
        publications = publications.filter(type__in=types)

    if enable_checkbox == 'on':
        if rinc and rinc == 'on':
            is_rinc = True
        else:
            is_rinc = False

        if vak and vak == 'on':
            is_vak = True
        else:
            is_vak = False

        if wos and wos == 'on':
            is_wos = True
        else:
            is_wos = False

        if scopus and scopus == 'on':
            is_scopus = True
        else:
            is_scopus = False

        publications = publications.filter(Q(is_rinc=is_rinc) &
                                           Q(is_vak=is_vak) &
                                           Q(is_wos=is_wos) &
                                           Q(is_scopus=is_scopus))

    grants_member = Grant.objects.filter(members__account=user.account).order_by('-date_start')
    grants_head = Grant.objects.filter(head__account=user.account).order_by('-date_start')

    if year_from and year_to:
        grants_member = grants_member.filter(date_start__year__gte=int(year_from), date_end__year__lte=int(year_to))
        grants_head = grants_head.filter(date_start__year__gte=int(year_from), date_end__year__lte=int(year_to))
    elif year_to:
        grants_member = grants_member.filter(date_start__year__lte=int(year_to))
        grants_head = grants_head.filter(date_end__year__lte=int(year_to))
    elif year_from:
        grants_member = grants_member.filter(date_end__year__gte=int(year_from))
        grants_head = grants_head.filter(date_start__year__gte=int(year_from))

    grants_head_ids = grants_head.values('id')
    grants_member = grants_member.exclude(id__in=grants_head_ids)

    conferences = Conference.objects.filter(author__user=user.account)
    if year_from and year_to:
        conferences = conferences.filter(publication__journal__date_start__year__gte=int(year_from),
                                         publication__journal__date_stop__year__lte=int(year_to))
    elif year_to:
        conferences = conferences.filter(publication__journal__date_start__year__lte=int(year_to))
    elif year_from:
        conferences = conferences.filter(publication__journal__date_stop__year__lte=int(year_from))

    conferences = conferences.order_by('-publication__journal__date_start')

    export_file = export_from_profile(publications, grants_member, grants_head, conferences)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename=export_profile_{}.docx'. \
        format(datetime.now().strftime('%d-%m-%Y'))
    export_file.save(response)
    return response


def profile_add_publication(request, username):
    current_user = get_object_or_404(User, username=username)

    if request.method == 'POST':
        form = PublicationForm(request.POST)
        if form.is_valid():
            publication = form.save()

            # handler for conference
            # TODO
            # handler for authors
            # TODO
            return redirect(profile, current_user)
    else:
        form = PublicationForm()

    context = {
        'form': form
    }
    return render(request, 'lmnad/profile_add_publication.html', context)


def profile_edit_publication(request, username):
    user = get_object_or_404(User, username=username)
    context = {
    }
    return render(request, 'lmnad/profile_edit_publication.html', context)


class EditProfileForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=200, required=False,
                             widget=forms.TextInput(attrs = {'class': 'form-control'}))
    is_subscribe = forms.BooleanField(label=u'Подписка на рассылку', required=False)
    text_ru = forms.CharField(widget=CKEditorUploadingWidget(), required=False, label=u'Текст страницы (ru)')
    text_en = forms.CharField(widget=CKEditorUploadingWidget(), required=False, label=u'Текст страницы (en)')
    photo = forms.ImageField(required=False, label=u'Фото в профиле')
    cv = forms.FileField(required=False, label=u'CV')


def edit_profile(request):
    current_user = request.user
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            is_subscribe = form.cleaned_data['is_subscribe']
            text_ru = form.cleaned_data['text_ru']
            text_en = form.cleaned_data['text_en']
            current_user.email = email

            try:
                form.data['photo-clear']
            except KeyError:
                photo_clear = False
            else:
                photo_clear = True

            try:
                form.data['cv-clear']
            except KeyError:
                cv_clear = False
            else:
                cv_clear = True

            photo = None
            cv = None
            if 'photo' in request.FILES:
                # save or update photo
                photo = Images.objects.create(file=request.FILES['photo'])
            if 'cv' in request.FILES:
                # save or update cv
                cv = request.FILES['cv']

            try:
                Account.objects.get(user_id=current_user.id)
            except Account.DoesNotExist:
                Account.objects.create(is_subscribe=is_subscribe,
                                       text_ru=text_ru,
                                       text_en=text_en,
                                       user_id=current_user.id,
                                       photo=photo,
                                       cv_file=cv)
            else:
                current_user.account.is_subscribe = is_subscribe
                current_user.account.text_ru = text_ru
                current_user.account.text_en = text_en
                if photo or photo_clear:
                    current_user.account.photo = photo
                if cv or cv_clear:
                    current_user.account.cv_file = cv
                current_user.account.save()
                current_user.save()

            return redirect(profile, current_user)
    else:
        try:
            current_user.account
        except Account.DoesNotExist:
            init = {}
        else:
            is_subscribe = current_user.account.is_subscribe
            text_ru = current_user.account.text_ru
            text_en = current_user.account.text_en
            init = {
                "email": current_user.email,
                "is_subscribe": is_subscribe,
                "text_ru": text_ru,
                "text_en": text_en,
                "cv": current_user.account.cv_file if current_user.account.cv_file else '',
                "photo": current_user.account.photo.file if current_user.account.photo else ''
            }

        form = EditProfileForm(initial=init)

    context = {
        'form': form
    }

    return render(request, 'lmnad/edit_profile.html', context)


def logout_view(request):
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


def contacts(request):
    contacts_page = Page.objects.get(name='contacts')

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
        'contacts': contacts_page,
        'form': form
    }

    return render(request, 'lmnad/contacts.html', context)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'lmnad/change_password.html', {
        'form': form
    })


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(max_length=100, label=u'Email')


def reset_password(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, 'Email don`t found')
            else:
                new_password = User.objects.make_random_password()
                user.set_password(new_password)
                user.save()

                subject = u'LMNAD, временный пароль'
                message = u'Ваш временный пароль для входа: ' + new_password
                try:
                    send_mail(subject, message, 'lmnad@nntu.ru', [email])
                except BadHeaderError:
                    return HttpResponse('Invalid header found')

                messages.success(request, 'Your new password send to ' + user.email)
            return redirect('reset_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = ResetPasswordForm()

    return render(request, 'lmnad/reset_password.html', {
        'form': form
    })


@require_http_methods(['GET'])
def pages(request, **kwargs):
    name = kwargs['name']

    project = Page.objects.get(name=name)

    context = {
        'project': project
    }
    return render(request, 'lmnad/project_details.html', context)
