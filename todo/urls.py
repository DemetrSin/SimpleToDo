from django.urls import path

from .views import (CreateToDoItemView, CreateToDoListView, ToDoListDetailView,
                    ToDoListView)

urlpatterns = [
    path('todo_list', ToDoListView.as_view(), name='todo_list'),
    path('create_todo_list', CreateToDoListView.as_view(), name='create_todo_list'),
    path('create_todo_item/<int:todo_list_id>', CreateToDoItemView.as_view(), name='create_todo_item'),
    path('todo_list/<int:pk>', ToDoListDetailView.as_view(), name='todo_list_detail')
]
