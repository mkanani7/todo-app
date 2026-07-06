from django.db import models

from accounts.models import User


class Todo(models.Model):
    user = models.ForeignKey(User, related_name="todos", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reminder_time = models.DateTimeField(null=True, blank=True)
    is_done = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
