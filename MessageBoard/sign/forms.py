# Импорт из Джанго
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError

# Импорт из ресурсов проекта
from .models import Code


# Форма регистрации
class SignupForm(UserCreationForm):
    email = forms.EmailField(label="Email")

    class Meta:
        model = User
        fields = ("username",
                  "email",
                  "password1",
                  "password2",
                  )


# Форма подтверждения регистрации
class ActivateForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', max_length=100)
    code = forms.CharField(label='Код подтверждения', max_length=10)

    def validate(self, value):
        # Проверяем введенные значения
        username = self.cleaned_data('username')
        code = self.cleaned_data('code')
        if not Code.objects.filter(user=username, code=code).exists():
            raise ValidationError('Неверное имя пользователя или код')


