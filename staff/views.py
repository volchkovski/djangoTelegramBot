from django.contrib.auth.mixins import (LoginRequiredMixin, UserPassesTestMixin)
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Employee, Chat


class HomePageView(TemplateView):
    template_name = 'home.html'


class ChatsView(LoginRequiredMixin, ListView):
    model = Chat
    template_name = 'chats.html'
    context_object_name = 'chat_list'


class EmployeesView(LoginRequiredMixin, ListView):
    model = Employee
    template_name = 'employees.html'
    context_object_name = 'employee_list'

    def get_chat(self):
        chat_pk = self.request.resolver_match.kwargs.get('chat_pk')
        return Chat.objects.get(pk=int(chat_pk))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chat = self.get_chat()
        if not chat:
            print('chat_pk is not supplied')
            return context

        context['chat'] = chat
        return context

class ChatCreateView(LoginRequiredMixin, CreateView):
    model = Chat
    template_name = 'chat_new.html'
    fields = ('name', 'chat_id',)

    def form_valid(self, form):
        form.instance.tl = self.request.user
        return super().form_valid(form)


class ChatUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Chat
    fields = ('name', 'chat_id',)
    template_name = 'chat_edit.html'

    def test_func(self):
        chat = self.get_object()
        return chat.tl == self.request.user


class ChatDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Chat
    template_name = 'chat_delete.html'
    success_url = reverse_lazy('chats')
    context_object_name = 'chat'

    def test_func(self):
        chat = self.get_object()
        return chat.tl == self.request.user


class EmployeeCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Employee
    template_name = 'employee_new.html'
    fields = ('tg_login',)

    def get_chat(self):
        chat_pk = self.request.resolver_match.kwargs.get('chat_pk')
        return Chat.objects.get(pk=int(chat_pk))

    def form_valid(self, form):
        chat = self.get_chat()
        if not chat:
            print('chat_pk is not supplied')
            return super().form_valid(form)

        form.instance.chat = chat
        return super().form_valid(form)

    def test_func(self):
        chat = self.get_chat()
        return chat.tl == self.request.user


class EmployeeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Employee
    fields = ('tg_login', 'work_status',)
    template_name = 'employee_edit.html'

    def test_func(self):
        employee = self.get_object()
        return employee.chat.tl == self.request.user


class EmployeeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Employee
    template_name = 'employee_delete.html'
    context_object_name = 'employee'

    def post(self, request, *args, **kwargs):
        chat_pk = request.resolver_match.kwargs.get('chat_pk')
        self.success_url = reverse_lazy('employees', kwargs={'chat_pk': chat_pk})
        return super().post(request, *args, **kwargs)

    def test_func(self):
        employee = self.get_object()
        return employee.chat.tl == self.request.user
