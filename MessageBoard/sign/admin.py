# Импорт из Джанго
from django.contrib import admin

# Импорт из ресурсов проекта
from .models import Code

admin.site.register(Code)