# Импорт из Джанго
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy

# Импорт из ресурсов проекта
from .models import Message, Reply
from .filters import MessageFilter, ReplyFilter
from .forms import MessageForm, ReplyForm


class MessageList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Message
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-post_time'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'messages.html'
    # Это имя списка, в котором будут лежать все объекты для обращения в html-шаблоне.
    context_object_name = 'messages'
    paginate_by = 3

    # Изменяем набор данных, который будет передан в шаблон.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context

    # Переопределяем функцию получения списка публикаций
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = MessageFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список публикаций
        return self.filterset.qs


class MessageDetail(DetailView):
    # Получаем информацию по отдельному объекту модели message
    model = Message
    # Используем шаблон message.html
    template_name = 'message.html'
    # Название объекта, в котором будет выбранная пользователем публикация
    context_object_name = 'message'


class ReplyList(LoginRequiredMixin, ListView):
    # Работаем с моделью reply
    model = Reply
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-post_time'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'replies.html'
    # Это имя списка, в котором будут лежать все объекты для обращения в html-шаблоне.
    context_object_name = 'replies'
    paginate_by = 3

    # Изменяем набор данных, который будет передан в шаблон.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        context['user'] = self.request.user.username
        return context

    # Переопределяем функцию получения списка публикаций
    def get_queryset(self):
        # Получаем обычный запрос и фильтруем его, чтобы выводились только ответы на объявления текущего пользователя
        queryset = super().get_queryset()
        # Фильтруем, чтобы выводились ответы только на объявления текущего пользователя
        queryset = queryset.filter(message__author=self.request.user)
        # Используем наш класс фильтрации.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = ReplyFilter(self.request.GET, request=self.request, queryset=queryset)
        # Возвращаем из функции отфильтрованный список публикаций
        return self.filterset.qs


class MessageCreate(LoginRequiredMixin, CreateView):
    # Указываем форму создания объявления
    form_class = MessageForm
    # Модель объявления
    model = Message
    # Шаблон, в котором используется форма
    template_name = 'message_edit.html'

    # Переопределяем метод сохранения формы для назначения текущего пользователя автором
    def form_valid(self, form):
        message = form.save(commit=False)
        message.author = self.request.user
        return super().form_valid(form)


# Представление для редактирования объявлений
class MessageUpdate(LoginRequiredMixin, UpdateView):
    # Указываем форму создания объявления
    form_class = MessageForm
    # Модель объявления
    model = Message
    # Шаблон, в котором используется форма
    template_name = 'message_edit.html'

    # Передаем юзера в форму
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        author = self.request.user
        # Передаем запрос в форму
        kwargs.update({"author": author})
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


# Представление для удаления объявлений
class MessageDelete(LoginRequiredMixin, DeleteView):
    # Модель объявления
    model = Message
    # Шаблон, в котором используется форма
    template_name = 'message_delete.html'
    # Адрес для перенаправления после удаления
    success_url = reverse_lazy('message_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class ReplyDelete(LoginRequiredMixin, DeleteView):
    # Модель отклика
    model = Reply
    # Шаблон, в котором используется форма
    template_name = 'reply_delete.html'
    # Адрес для перенаправления после удаления
    success_url = reverse_lazy('reply_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.message.author != self.request.user:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


def confirm(request, *args, **kwargs):
    # Отклик, с которым работаем
    reply = Reply.objects.get(pk=kwargs['pk'])
    # Изменяем состояние отклика
    reply.confirmed = True
    reply.save(update_fields=['confirmed'])
    return redirect(reverse_lazy('reply_list'))


class ReplyCreate(LoginRequiredMixin, CreateView):
    # Указываем форму создания отклика
    form_class = ReplyForm
    # Модель объявления
    model = Reply
    # Шаблон, в котором используется форма
    template_name = 'reply.html'
    # Ссылка на страницу подтверждения отправки отклика
    success_url = '/successful_reply/'

    # Переопределяем метод сохранения формы для назначения текущего пользователя автором
    def form_valid(self, form):
        reply = form.save(commit=False)
        reply.author = self.request.user
        reply.message = Message.objects.get(pk=self.kwargs['message_pk'])
        return super().form_valid(form)

    # Передаем юзера и первичный ключ объявления в форму
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        author = self.request.user
        message_id = self.kwargs['message_pk']
        kwargs.update({'author': author, 'message_pk': message_id})
        return kwargs

    # Добавляем в контекст объявление, на которое создается отклик, для формирования шаблона
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = Message.objects.get(pk=self.kwargs['message_pk'])
        return context