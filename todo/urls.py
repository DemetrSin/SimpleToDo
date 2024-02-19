from django.urls import path

from .views import (
    CreateToDoItemView,
    CreateToDoListView,
    ToDoListDetailView,
    ToDoListView,
    ToDoListDeleteView,
    ToDoItemUpdateView
)

urlpatterns = [
    path('todo_list', ToDoListView.as_view(), name='todo_list'),
    path('create_todo_list', CreateToDoListView.as_view(), name='create_todo_list'),
    path('create_todo_item/<int:todo_list_id>', CreateToDoItemView.as_view(), name='create_todo_item'),
    path('todo_list/<int:pk>', ToDoListDetailView.as_view(), name='todo_list_detail'),
    path('todo_list/<int:pk>/delete', ToDoListDeleteView.as_view(), name='todo_list_delete'),
    path('update_todo_item/<int:pk>', ToDoItemUpdateView.as_view(), name='update_todo_item')
]
