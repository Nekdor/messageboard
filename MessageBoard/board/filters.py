# Импорт из Джанго
from django_filters import FilterSet, DateFilter, ModelChoiceFilter
from django.forms.widgets import DateInput

# Импорт из ресурсов проекта
from .models import Message, Reply


# Создаем свой набор фильтров для модели Message.
class MessageFilter(FilterSet):

    # Создаем фильтр по дате
    date_gt = DateFilter(field_name='post_time',
                         lookup_expr='gt',
                         label='Опубликовано позже, чем',
                         widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        # Модель в которой будем фильтровать записи.
        model = Message
        # Описываем по каким полям модели будет производиться фильтрация.
        fields = {
            # поиск по названию
            'title': ['icontains'],
            # поиск по названию категории
            'category': ['exact'],
            # поиск по имени автора
            'author__username': ['icontains'],
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['title__icontains'].label = 'Название содержит:'
        self.filters['category'].label = 'Категория:'
        self.filters['author__username__icontains'].label = 'Автор:'


# Функция, возвращающая набор объявлений текущего пользователя
def user_message_set(request):
    if request is None:
        return Message.objects.none()
    return Message.objects.filter(author=request.user)


# Создаем свой набор фильтров для модели Post.
class ReplyFilter(FilterSet):
    # Фильтруем по объявлениям, при этом берем только объявления за авторством текущего пользователя.
    message = ModelChoiceFilter(
        queryset=user_message_set,
        label='Отклики на твои объявления:',
        empty_label='Все объявления'
    )

    class Meta:
        # Модель в которой будем фильтровать записи.
        model = Reply
        # Описываем по каким полям модели будет производиться фильтрация.
        fields = {
            # поиск по объявлению
            'message',
        }
