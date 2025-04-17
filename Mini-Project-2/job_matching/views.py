from django.shortcuts import render
from rest_framework import generics, status, permissions, filters, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Job, JobApplication, JobMatch, SavedJob, Resume, ResumeAnalysis, ResumeFeedback
from .serializers import (
    JobSerializer,
    JobApplicationSerializer,
    JobMatchSerializer,
    SavedJobSerializer,
    JobApplicationCreateSerializer,
    JobSearchSerializer,
    ResumeSerializer,
    ResumeAnalysisSerializer,
    ResumeFeedbackSerializer
)
from .tasks import calculate_job_match, analyze_resume

class JobListView(generics.ListCreateAPIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['job_type', 'experience_level', 'location']

    def get_queryset(self):
        return Job.objects.filter(is_active=True)

    def perform_create(self, serializer):
        serializer.save(recruiter=self.request.user)

class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Job.objects.filter(is_active=True)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

class JobApplicationListView(generics.ListCreateAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return JobApplication.objects.filter(job__recruiter=user)
        return JobApplication.objects.filter(applicant=user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return JobApplicationCreateSerializer
        return JobApplicationSerializer

    def perform_create(self, serializer):
        application = serializer.save(applicant=self.request.user)
        analyze_resume.delay(application.resume.id)

class JobApplicationDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return JobApplication.objects.filter(job__recruiter=user)
        return JobApplication.objects.filter(applicant=user)

class JobMatchListView(generics.ListAPIView):
    serializer_class = JobMatchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == user.Role.RECRUITER:
            return JobMatch.objects.filter(job__recruiter=user)
        return JobMatch.objects.filter(resume__user=user)

class SavedJobListView(generics.ListCreateAPIView):
    serializer_class = SavedJobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SavedJob.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SavedJobDetailView(generics.DestroyAPIView):
    serializer_class = SavedJobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SavedJob.objects.filter(user=self.request.user)

class JobSearchView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = JobSearchSerializer(data=request.data)
        if serializer.is_valid():
            jobs = Job.objects.filter(is_active=True)
            
            if serializer.validated_data.get('title'):
                jobs = jobs.filter(title__icontains=serializer.validated_data['title'])
            if serializer.validated_data.get('location'):
                jobs = jobs.filter(location__icontains=serializer.validated_data['location'])
            if serializer.validated_data.get('job_type'):
                jobs = jobs.filter(job_type=serializer.validated_data['job_type'])
            if serializer.validated_data.get('experience_level'):
                jobs = jobs.filter(experience_level=serializer.validated_data['experience_level'])
            if serializer.validated_data.get('skills'):
                jobs = jobs.filter(skills_required__contains=serializer.validated_data['skills'])
            if serializer.validated_data.get('salary_min'):
                jobs = jobs.filter(salary_min__gte=serializer.validated_data['salary_min'])
            if serializer.validated_data.get('salary_max'):
                jobs = jobs.filter(salary_max__lte=serializer.validated_data['salary_max'])

            serializer = JobSerializer(jobs, many=True)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResumeViewSet(generics.ListCreateAPIView):
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        analyze_resume.delay(serializer.instance.id)

class ResumeDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

class ResumeAnalysisView(generics.RetrieveAPIView):
    serializer_class = ResumeAnalysisSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ResumeAnalysis.objects.filter(resume__user=self.request.user)

class ResumeFeedbackView(generics.ListAPIView):
    serializer_class = ResumeFeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ResumeFeedback.objects.filter(resume__user=self.request.user)
