from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Resume, ResumeAnalysis, Skill, Experience, Education
from .serializers import (
    ResumeSerializer,
    ResumeUploadSerializer,
    ResumeAnalysisSerializer,
    SkillSerializer,
    ExperienceSerializer,
    EducationSerializer,
    ResumeFeedbackSerializer
)
from .tasks import process_resume

# Create your views here.

class ResumeListView(generics.ListCreateAPIView):
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        resume = serializer.save(user=self.request.user)
        # Trigger background task for resume processing
        process_resume.delay(resume.id)

class ResumeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

class ResumeUploadView(generics.CreateAPIView):
    serializer_class = ResumeUploadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        resume = serializer.save(user=self.request.user)
        # Trigger background task for resume processing
        process_resume.delay(resume.id)

class ResumeAnalysisView(generics.RetrieveAPIView):
    serializer_class = ResumeAnalysisSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        resume = get_object_or_404(Resume, id=self.kwargs['pk'], user=self.request.user)
        return resume.analysis

class SkillListView(generics.ListAPIView):
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Skill.objects.all()

class ExperienceListView(generics.ListCreateAPIView):
    serializer_class = ExperienceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Experience.objects.filter(resume__user=self.request.user)

    def perform_create(self, serializer):
        resume = get_object_or_404(Resume, id=self.kwargs['resume_id'], user=self.request.user)
        serializer.save(resume=resume)

class EducationListView(generics.ListCreateAPIView):
    serializer_class = EducationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Education.objects.filter(resume__user=self.request.user)

    def perform_create(self, serializer):
        resume = get_object_or_404(Resume, id=self.kwargs['resume_id'], user=self.request.user)
        serializer.save(resume=resume)

class ResumeFeedbackView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ResumeFeedbackSerializer(data=request.data)
        if serializer.is_valid():
            resume = get_object_or_404(Resume, id=serializer.validated_data['resume_id'], user=request.user)
            analysis = resume.analysis
            analysis.feedback = serializer.validated_data['feedback']
            analysis.score = serializer.validated_data['score']
            analysis.save()
            return Response({'message': 'Feedback submitted successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
