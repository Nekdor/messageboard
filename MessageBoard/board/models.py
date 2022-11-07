from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField


# Модель объявления
class Message(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    CATEGORIES = [
        ('tanks', 'Танки'),
        ('healers', 'Хилы'),
        ('dd', 'ДД'),
        ('merchants', 'Торговцы'),
        ('guildmasters', 'Гилдмастеры'),
        ('questgivers', 'Квестгиверы'),
        ('smiths', 'Кузнецы'),
        ('tanners', 'Кожевники'),
        ('potionmasters', 'Зельевары'),
        ('spellmasters', 'Мастера заклинаний'),
    ]

    category = models.CharField(max_length=100, choices=CATEGORIES, default='tanks')
    title = models.CharField(max_length=100, blank=True, null=False)
    content = RichTextUploadingField(blank=True, null=True, extra_plugins=['youtube'])
    post_time = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('message_detail', args=[str(self.id)])

    def __str__(self):
        return str(self.id) + '. ' + self.title


class Reply(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default = None)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    text = models.TextField()
    confirmed = models.BooleanField(default=False)
    post_time = models.DateTimeField(auto_now_add=True)

    def confirm(self):
        self.confirmed = True
        self.save()

    def __str__(self):
        preview_len = 50
        preview = self.text[:preview_len]
        ending = '' if len(preview) <= preview_len else '...'

        return str(self.id) + '. ' + preview + ending
