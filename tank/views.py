# -*- coding: utf-8 -*-
from django.shortcuts import render


def tank(request):
    """ Tank main page """
    context = {}

    return render(request, 'tank/tank.html', context)

