from django.template import loader
from django.http import HttpResponse


def app(request):
    return HttpResponse(loader.get_template('index.html').render())