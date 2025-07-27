from django.shortcuts import render
from django.core.mail import send_mail,mail_admins,BadHeaderError
from .tasks import notify_user
from django.views.decorators.cache import cache_page
import requests


@cache_page(1*60)
def say_hello(request):
    requests.get("http://httpbin.org/delay/2")
    return render(request, 'hello.html', {'name': 'Mosh'})
