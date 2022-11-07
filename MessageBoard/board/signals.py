# Импорт из Джанго
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# Импорт из ресурсов проекта
from .models import Reply

# Импорт стандартных пакетов
import os


# Сигнал, отправляющий сообщение автору объявления при добавлении отклика или автору отклика при его принятии
@receiver(post_save, sender=Reply)
def notify_message_author(sender, instance, created, update_fields, **kwargs):
    # Объявление, на которое получен отклик
    message = instance.message
    # Ссылка на объявление
    link = f'http://127.0.0.1:8000/{message.id}/'
    # Переменная-флаг, оказывает, надо ли отправлять письмо
    send = False
    # Случай создания нового отклика
    if created:
        send = True
        # Тема письма
        subject = f'Новый отклик на объявление {message.title}'
        # Название шаблона оповещения о новом отклике
        template = 'new_reply'
        # Текст письма
        body = f'Здравствуй, {message.author.username}! На твое объявление {message.title} получен новый отклик.'
        # Адресат - автор объявления
        to = message.author.email
    # Случай принятия отклика
    elif update_fields and 'confirmed' in update_fields and instance.confirmed:
        send = True
        # Тема письма
        subject = f'Принят отклик на объявление {message.title}'
        # Название шаблона оповещения о принятии отклика
        template = 'reply_confirmed'
        # Текст письма
        body = f'Здравствуй, {message.author.username}! Твой отклик на объявление {message.title} принят.'
        # Адресат - автор отклика
        to = instance.author.email
    # Формируем и отправляем сообщение только если произошло соответствующее событие и у адресата существует почта
    if send and to:
        # Получаем наш html
        html_content = render_to_string(
            template + '.html',
            {
                'reply': instance,
                'link': link,
            }
        )

        msg = EmailMultiAlternatives(
            # В тему письма выносим заголовок публикации
            subject=subject,
            # Сообщение пользователю
            body=body,
            # Почта, с которой отправляем письмо
            from_email=str(os.getenv('EMAIL_HOST_USER')) + '@yandex.ru',
            to=[to]  # почта получателя
        )
        # Добавляем html
        msg.attach_alternative(html_content, 'text/html')
        # Отсылаем
        msg.send()
