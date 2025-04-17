from django.urls import path
from .views import (
    JobListView,
    JobDetailView,
    JobApplicationListView,
    JobApplicationDetailView,
    ResumeViewSet,
    ResumeDetailView,
    ResumeAnalysisView,
    ResumeFeedbackView,
    SavedJobListView,
    SavedJobDetailView,
    JobSearchView
)

urlpatterns = [
    path('jobs/', JobListView.as_view(), name='job-list'),
    path('jobs/<int:pk>/', JobDetailView.as_view(), name='job-detail'),
    path('applications/', JobApplicationListView.as_view(), name='application-list'),
    path('applications/<int:pk>/', JobApplicationDetailView.as_view(), name='application-detail'),
    path('resumes/', ResumeViewSet.as_view(), name='resume-list'),
    path('resumes/<int:pk>/', ResumeDetailView.as_view(), name='resume-detail'),
    path('resumes/<int:pk>/analysis/', ResumeAnalysisView.as_view(), name='resume-analysis'),
    path('resumes/<int:pk>/feedback/', ResumeFeedbackView.as_view(), name='resume-feedback'),
    path('saved-jobs/', SavedJobListView.as_view(), name='saved-job-list'),
    path('saved-jobs/<int:pk>/', SavedJobDetailView.as_view(), name='saved-job-detail'),
    path('jobs/search/', JobSearchView.as_view(), name='job-search'),
] 