from django.shortcuts import render
from django.views.defaults import page_not_found, server_error
#from django.template import RequestContext

# Create your views here.


def landing_page(request):
    return render(request, 'landing/index.html')

# Error 404
def Error_404(request, exception):
    return render(request, 'error/404.html', status=404)

# Error 500
def Error_500(request):
    return render(request, 'error/500.html', status=500)
