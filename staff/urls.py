from django.urls import path
from .views import (HomePageView, ChatsView, EmployeesView,
                    ChatCreateView, EmployeeCreateView,
                    ChatUpdateView, ChatDeleteView,
                    EmployeeUpdateView, EmployeeDeleteView)

urlpatterns = [
    path('chats/<int:chat_pk>/employees/<int:pk>/delete/', EmployeeDeleteView.as_view(), name='employee_delete'),
    path('chats/<int:chat_pk>/employees/<int:pk>/edit/', EmployeeUpdateView.as_view(), name='employee_edit'),
    path('chats/<int:pk>/delete', ChatDeleteView.as_view(), name='chat_delete'),
    path('chats/<int:pk>/edit', ChatUpdateView.as_view(), name='chat_edit'),
    path('chats/<int:chat_pk>/employees/new/', EmployeeCreateView.as_view(), name='employee_new'),
    path('chats/new/', ChatCreateView.as_view(), name='chat_new'),
    path('chats/<int:chat_pk>/employees/', EmployeesView.as_view(), name='employees'),
    path('chats/', ChatsView.as_view(), name='chats'),
    path('', HomePageView.as_view(), name='home'),
]
