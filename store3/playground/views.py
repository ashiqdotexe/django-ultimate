from django.shortcuts import render
from django.core.mail import send_mail,mail_admins,BadHeaderError

def say_hello(request):
    try:
        send_mail("Hello From Django", "Hello this is from django", "admin@admin.com", ["ashiqurrahman.sohan.muslim@gmail.com"])
    except BadHeaderError:
        pass 
    return render(request, 'hello.html', {'name': 'Mosh'})
