from django.shortcuts import render
from django.template import RequestContext

# Create your views here.


def LandingPage(request):
    return render(request, 'landing/index.html')
