from django.urls import path
from . import views

urlpatterns = [
    # Resume endpoints
    path('resumes/', views.ResumeListView.as_view(), name='resume-list'),
    path('resumes/<int:pk>/', views.ResumeDetailView.as_view(), name='resume-detail'),
    path('resumes/upload/', views.ResumeUploadView.as_view(), name='resume-upload'),
    
    # Analysis endpoints
    path('resumes/<int:pk>/analysis/', views.ResumeAnalysisView.as_view(), name='resume-analysis'),
    path('resumes/<int:pk>/feedback/', views.ResumeFeedbackView.as_view(), name='resume-feedback'),
    
    # Skills endpoints
    path('skills/', views.SkillListView.as_view(), name='skill-list'),
    
    # Experience endpoints
    path('resumes/<int:resume_id>/experiences/', views.ExperienceListView.as_view(), name='experience-list'),
    
    # Education endpoints
    path('resumes/<int:resume_id>/educations/', views.EducationListView.as_view(), name='education-list'),
] 