from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, response, status

from note.serializer import NoteSerializer
from note.models import Note

# Create your views here.
class NoteViewSet(viewsets.GenericViewSet):
    permission_classes = []
    def home_note(self,request):
        return render(request, 'base.html')
    def create_note(self,request):
        # if request.user:
        req_data = request.data
        req_data["created_date"] = datetime.now()
        if Note.objects.filter(title__icontains = req_data.get('title')).exists():
            return response.Response(data={
                "data":[],
                "message":"Already similar title post exists"}, status=status.HTTP_400_BAD_REQUEST)
        post_serialize = NoteSerializer(data=req_data)
        if post_serialize.is_valid():
            post_serialize.save()
            return response.Response(data={
                "data": post_serialize.data,
                "message": "Note Created"
                },
                status=status.HTTP_201_CREATED
            )
        return response.Response(
            {
                "data": post_serialize.error_messages,
                "message": "Not Created"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # return HttpResponse("Create note")

    def list_note(self,request):
        title = request.GET.get("title")
        note_id = int(request.GET.get("note_id", 0))
        compelted = request.GET.get("is_completed", False) in {"true", True}
        if note_id:
            note_data = Note.objects.filter(id=note_id)
        elif title:
            note_data = Note.objects.filter(title__icontains=title)
        elif compelted:
            note_data = Note.objects.filter(is_completed=compelted)
        else:
            note_data = Note.objects.all()
        req_data = NoteSerializer(note_data, many=True)
        return response.Response(data={
            "data": req_data.data,
            "message": "Note list Fetched"
            },
        status=status.HTTP_200_OK)

    def delete_note(self,request, pk):
        note_data = Note.objects.filter(id=pk).first()
        if note_data:
            note_data.delete()
            return response.Response({
                "data": [],
                "message": "Deleted Success"
            }, status=status.HTTP_200_OK)
        return response.Response({
            "data": [],
            "message": "No Note Found!!"
        }, status=status.HTTP_400_BAD_REQUEST)

    def edit_note(self,request, pk):
        note_data = Note.objects.filter(id=pk).first()
        if note_data:
            # note_data.update(**data)
            req_data = NoteSerializer(note_data, data=request.data, partial=True)
            if req_data.is_valid():
                req_data.save()
                return response.Response({
                    "data": req_data.data,
                    "message": "Data is updated"
                }, status=status.HTTP_200_OK)
        return response.Response({
            "data": [],
            "message": "No Note Found!"
        }, status=status.HTTP_400_BAD_REQUEST)