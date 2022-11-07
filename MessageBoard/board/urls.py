# Импорт из Джанго
from django.urls import path

# Импорт из ресурсов проекта
from .views import MessageList, MessageDetail, ReplyList, MessageCreate, MessageUpdate, MessageDelete, ReplyDelete, \
    confirm, ReplyCreate


urlpatterns = [
    path('', MessageList.as_view(), name='message_list'),
    path('<int:pk>/', MessageDetail.as_view(), name='message_detail'),
    path('<int:pk>/edit/', MessageUpdate.as_view(), name='message_update'),
    path('<int:pk>/delete/', MessageDelete.as_view(), name='message_delete'),
    path('<int:message_pk>/reply/', ReplyCreate.as_view(), name='reply'),
    path('replies/', ReplyList.as_view(), name='reply_list'),
    path('replies/<int:pk>/delete/', ReplyDelete.as_view(), name='reply_delete'),
    path('replies/<int:pk>/confirm/', confirm, name='reply_confirm'),
    path('create/', MessageCreate.as_view(), name='message_create'),
    ]


