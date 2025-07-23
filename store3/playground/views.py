from django.shortcuts import render
from django.core.mail import send_mail,mail_admins,BadHeaderError
from .tasks import notify_user
def say_hello(request):
    notify_user.delay("Ashiq")
    return render(request, 'hello.html', {'name': 'Mosh'})
