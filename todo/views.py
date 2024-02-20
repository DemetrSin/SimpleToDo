from django.db.models import Q
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, DeleteView, UpdateView
from django.contrib.auth.models import User

from .models import ToDoItem, ToDoList
from .forms import AddUserForm


class ToDoListView(ListView):
    model = ToDoList
    template_name = 'todo/todo_list.html'
    context_object_name = 'todo_list'

    def get_queryset(self):
        return ToDoList.objects.filter(Q(user=self.request.user) | Q(shared_with=self.request.user))


class CreateToDoListView(CreateView):
    model = ToDoList
    fields = ['title']
    template_name = 'todo/create_todo_list.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(f"create_todo_item", kwargs={'todo_list_id': self.object.id})


class ToDoListDetailView(DetailView):
    model = ToDoList
    template_name = 'todo/todo_list_detail.html'
    context_object_name = 'todo_list'


class ToDoListDeleteView(DeleteView):
    model = ToDoList
    template_name = 'todo/delete_todo_list.html'
    success_url = reverse_lazy('todo_list')


class CreateToDoItemView(CreateView):
    model = ToDoItem
    template_name = 'todo/create_todo_item.html'
    fields = ['title', 'description', 'priority', 'due_date', 'status']
    success_url = reverse_lazy('todo_list')

    def form_valid(self, form):
        todo_list_id = self.kwargs['todo_list_id']
        todo_list = get_object_or_404(ToDoList, pk=todo_list_id)
        form.instance.todo_list = todo_list
        return super().form_valid(form)


class ToDoItemUpdateView(UpdateView):
    model = ToDoItem
    fields = ['title', 'description', 'priority', 'due_date', 'status']
    template_name = 'todo/update_todo_item.html'
    success_url = reverse_lazy('todo_list')


class ToDoItemDeleteView(DeleteView):
    model = ToDoItem
    template_name = 'todo/delete_todo_list.html'
    success_url = reverse_lazy('todo_list')


class AddUserToToDoListView(View):
    template_name = 'todo/add_user.html'

    def get(self, request, *args, **kwargs):
        form = AddUserForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = AddUserForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username_or_email']
            todo_list_id = self.kwargs['todo_list_id']
            try:
                todo_list = ToDoList.objects.get(pk=todo_list_id)
            except ToDoList.DoesNotExist:
                return HttpResponseBadRequest('Todo DoesNotExist))')

            user = User.objects.filter(Q(username=username_or_email) | Q(email=username_or_email)).first()
            if user:
                todo_list.shared_with.add(user)
                return redirect(reverse('todo_list'))
            else:
                form.add_error('username_or_email', "user doesn't exist")
        return render(request, self.template_name, {'form': form})
