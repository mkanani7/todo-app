from rest_framework import serializers

from todos.models import Todo


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = [
            "id",
            "title",
            "description",
            "created_at",
            "reminder_time",
            "is_done",
        ]
        read_only_fields = ["id", "created_at", "is_done"]
