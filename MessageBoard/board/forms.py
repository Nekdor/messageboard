# Импорт из Джанго
from django import forms
from django.core.exceptions import ValidationError

# Импорт из ресурсов проекта
from .models import Message, Reply


# Класс формы для создания и редактирования объявления
class MessageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        # """ Добавляем автора объявления в конструктор класса"""
        # self.author = kwargs.pop('author')
        super().__init__(*args, **kwargs)
        self.fields['title'].label = "Заголовок:"
        self.fields['category'].label = "Категория:"
        self.fields['content'].label = "Содержание:"

    class Meta:
        model = Message
        fields = ['title', 'category', 'content']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')
        if title == '':
            raise ValidationError('Заголовок не должен быть пустым!')
        if content == '':
            raise ValidationError('Содержание не должно быть пустым!')
        return cleaned_data


# Класс формы для создания отклика
class ReplyForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        """ Добавляем автора отклика и объявление в конструктор класса"""
        self.author = kwargs.pop('author')
        self.message = Message.objects.get(pk=kwargs.pop('message_pk'))
        super().__init__(*args, **kwargs)
        self.fields['text'].label = 'Введи ответ:'

    class Meta:
        model = Reply
        fields = ['text']

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get('text')
        if text == '':
            raise ValidationError('Отклик не должен быть пустым!')
        if self.author == self.message.author:
            raise ValidationError('Нельзя ответить на собственное объявление!')
        return cleaned_data
