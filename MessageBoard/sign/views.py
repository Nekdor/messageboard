# Импорт из Джанго
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, FormView
from django.core.mail import send_mail

# Импорт стандартных пакетов
import string
import random
import os

# Импорт из ресурсов проекта
from .models import Code
from .forms import SignupForm, ActivateForm


# Представление для регистрации
class SignupView(CreateView):
    model = User
    form_class = SignupForm
    success_url = '/activate/'
    template_name = 'sign/signup.html'

    # Переопределяем метод сохранения формы для временной деактивации аккаунта и отправки кода
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        code = Code.objects.create(user=user, code=''.join(random.choices(string.ascii_uppercase + string.digits, k=5)))
        code.save()
        send_mail(
            'Подтверждение регистрации',
            f'Приветствуем, {user.username}! Твой код для подтверждения регистрации: {code.code}',
            str(os.getenv('EMAIL_HOST_USER')) + '@yandex.ru',
            [user.email],
            fail_silently=False,
        )
        self.request.session['username'] = user.username
        return super().form_valid(form)


class ActivateView(FormView):
    template_name = 'sign/activate.html'
    form_class = ActivateForm
    success_url = '/replies/'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        user = User.objects.get(username=username)
        user.is_active = True
        user.save()
        Code.objects.get(user__username=username).delete()
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        initial['username'] = self.request.session['username']
        return initial

