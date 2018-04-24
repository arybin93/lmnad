# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render

from lmnad.models import Project
from tank.models import Experiment


def tank(request):
    """ Tank main page """
    query = request.GET.get('query', None)
    page = request.GET.get('page', 1)

    if query:
        experiments_list = Experiment.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    else:
        experiments_list = Experiment.objects.all()

    paginator = Paginator(experiments_list, 15)

    try:
        experiments = paginator.page(page)
    except PageNotAnInteger:
        experiments = paginator.page(1)
    except EmptyPage:
        experiments = paginator.page(paginator.num_pages)

    context = {
        'experiments': experiments,
        'project': Project.objects.get(name='wave_tank')
    }
    return render(request, 'tank/experiments.html', context)


def tank_exp_detail(request, pk):
    experiment = Experiment.objects.get(pk=pk)

    context = {
        'experiment': experiment,
        'project': Project.objects.get(name='wave_tank'),
        'images': experiment.images.filter(is_schema=False)
    }
    return render(request, 'tank/experiment_details.html', context)