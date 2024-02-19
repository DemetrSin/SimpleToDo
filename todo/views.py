from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, DeleteView, UpdateView

from .models import ToDoItem, ToDoList


class ToDoListView(ListView):
    model = ToDoList
    template_name = 'todo/todo_list.html'
    context_object_name = 'todo'

    def get_queryset(self):
        return ToDoList.objects.filter(user=self.request.user)


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
    template_name = 'todo/todo_list_delete.html'
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
    template_name = 'todo/todo_item_update.html'
    success_url = reverse_lazy('todo_list')
