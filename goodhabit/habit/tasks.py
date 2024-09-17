from django.core.mail import send_mail
from celery import shared_task
from .notifications import send_telegram_message

@shared_task
def send_notification_task(chat_id, message):
    send_telegram_message(chat_id, message)

@shared_task
def send_reminder_email(user_id, habit_id):
    from django.contrib.auth.models import User
    from .models import Habit

    user = User.objects.get(id=user_id)
    habit = Habit.objects.get(id=habit_id)

    # Отправить письмо напоминание
    send_mail(
        'Habit Reminder',
        f'Dear {user.username}, don’t forget to {habit.action} at {habit.time} in {habit.place}.',
        'from@example.com',
        [user.email],
        fail_silently=False,
    )
