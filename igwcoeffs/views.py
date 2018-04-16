# -*- coding: utf-8 -*-
from django.shortcuts import render


def igwcoeffs(request):
    """ IGW Coeffs calculator, main page """
    context = {}

    return render(request, 'igwcoeffs/tank.html', context)


def igwcoeffs_about(request):
    """ IGW Coeffs calculator, about page"""
    context = {}

    return render(request, 'igwcoeffs/about.html', context)
