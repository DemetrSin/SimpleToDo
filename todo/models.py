from django.conf import settings
from django.db import models

PRIORITY_CHOICES = (
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
)

STATUS_CHOICES = (
    ('todo', 'To Do'),
    ('in_progress', 'In Progress'),
    ('done', 'Done'),
)


class ToDoList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=128, unique=True)
    shared_with = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='shared_with')

    def __str__(self):
        return f"{self.pk} > {self.title}"


class ToDoItem(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    priority = models.CharField(max_length=15, choices=PRIORITY_CHOICES)
    created_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    todo_list = models.ForeignKey(ToDoList, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.pk} > {self.title}"
