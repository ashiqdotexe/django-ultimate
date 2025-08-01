from django.shortcuts import render
from django.core.mail import send_mail,mail_admins,BadHeaderError
from .tasks import notify_user
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
import requests
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


class SayHello(APIView):
    permission_classes = [AllowAny]
    @method_decorator(cache_page(5*60))
    def get(self, request):
        requests.get("http://httpbin.org/delay/2")
        return render(request, 'hello.html', {'name': 'Mosh'})


    
