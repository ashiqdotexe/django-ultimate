from django.shortcuts import render
from django.core.mail import send_mail,mail_admins,BadHeaderError
from templated_mail.mail import BaseEmailMessage
def say_hello(request):
    try:
        message = BaseEmailMessage(
            template_name= "emails/hello.html",
            context= {"name":"SOHAN"}
        )
        message.send(["ashiq@gmail.com"])
    except BadHeaderError:
        pass 
    return render(request, 'hello.html', {'name': 'Mosh'})
