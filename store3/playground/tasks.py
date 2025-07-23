from celery import shared_task
from time import sleep

@shared_task
def notify_user(message):
    print("Sending 10k messages")
    print(message)
    sleep(5)
    print(f'{message} sent successfully') 