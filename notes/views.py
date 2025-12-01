from django.shortcuts import render
from rest_framework.decorators import APIView
from rest_framework.response import Response
from .serializers import *
from .models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .ai.summarizer import *
from .ai.rewriter import *
from .ai.keywords import *
from .ai.titlegen import *
import html
# Create your views here.

class NotesView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes =  [IsAuthenticated]
    def post(self, request):
        serializers = NoteSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save(owner=request.user)
            return Response(serializers.data, status=201)
        return Response(serializers.errors, status=400)
    
    def get(self, request):
        serializers = NoteSerializer(Note.objects.filter(owner=request.user), many=True)
        return Response(serializers.data, status=200)
    
        
class NotesDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        try:
            note_object = Note.objects.get(id=id, owner=request.user) 
            serializers = NoteSerializer(note_object)
            return Response(serializers.data, status=200)
        except Note.DoesNotExist:
            return Response({"message":"doesnt exist"}, status=404)
        
    
    
    def patch(self, request, id):
        try:
            note = Note.objects.get(id=id, owner=request.user)
            serializers = NoteSerializer(note, data=request.data, partial=True)
            if serializers.is_valid():
                serializers.save()
                return Response({"message":"notes Update"}, status=200)
        except Note.DoesNotExist:
            return Response({"error":"note does not exist"},status=400)
    
    def delete(self, request, id):
        try:
            note = Note.objects.get(id=id, owner=request.user)
            note.delete()
            return Response( {"message":"Note deleted"},status=200)
        except Note.DoesNotExist:
            return Response({"error":"note does not exist"}, status=400)
            

class NoteSummarizer(APIView):
    def post(self, request, id):
        try:
            note = Note.objects.get(id=id, owner=request.user)
            summary = summarize_text(note.content)
            return Response({
                "id": id,
                "title": note.title,
                "original": note.content,
                "summary": summary
            }, status=200)
        except Note.DoesNotExist:
            return Response({"message":"Notes doesn't exist"}, status=404)
        
class ParaphraseAPI(APIView):
    def post(self, request):
        note = request.data.get("text", "")
        if not note:
            return Response({"message":"Text require"}, status=400)
        paraphrased_text = paraphrase_text(note)
        return Response({"paraphrased":paraphrased_text}, status=200)
        
class KeywordsApi(APIView):
    def post(self, request):
        note = request.data.get("text")
        if not note:
            return Response({"error":"Text mandatory"}, status=400)
        keywords =extract_keywords(note)
        return Response({"note":list(keywords)}, status=200)
    
class TitleGenAPi(APIView):
    def post(self, request):
        title = request.data.get("text")
        if not title:
            return Response({"error":"Text mandatory"}, status=400)
        generated_title = createTitle(title)
        clean_title = html.unescape(generated_title)
        return Response({"note": clean_title}, status=200)   