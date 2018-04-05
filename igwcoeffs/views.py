from django.shortcuts import render


def igwcoeffs(request):
    """ IGW Coeffs calculator, main page """
    context = {}

    return render(request, 'igwcoeffs/igwcoeffs.html', context)


def igwcoeffs_about(request):
    """ IGW Coeffs calculator, about page"""
    context = {}

    return render(request, 'igwcoeffs/about.html', context)
