# Импорт из Джанго
from django.contrib import admin

# Импорт из ресурсов проекта
from .models import Message, Reply


admin.site.register(Message)
admin.site.register(Reply)