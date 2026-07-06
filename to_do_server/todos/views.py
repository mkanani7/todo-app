from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from todos.models import Todo
from todos.serializers import TodoSerializer


class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["patch"], url_path="toggle-done")
    def toggle_done(self, request, pk=None):
        todo = self.get_object()
        todo.is_done = not todo.is_done
        todo.save(update_fields=["is_done"])
        serializer = self.get_serializer(todo)
        return Response(serializer.data)
