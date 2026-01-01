from rest_framework import serializers
from user.serializer import UserSerializer
from note.models import Note

class NoteSerializer(serializers.ModelSerializer):
    # author = UserSerializer()
    class Meta:
        model = Note
        fields = ("id", "title", "content", "created_date", "is_completed")