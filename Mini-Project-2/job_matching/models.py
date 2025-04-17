from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class Job(models.Model):
    # Simple choices for job type and experience level
    JOB_TYPES = [
        ('FT', 'Full Time'),
        ('PT', 'Part Time'),
        ('CT', 'Contract'),
        ('IN', 'Internship'),
        ('RM', 'Remote')
    ]
    
    EXPERIENCE_LEVELS = [
        ('EN', 'Entry Level'),
        ('JR', 'Junior'),
        ('MD', 'Mid Level'),
        ('SR', 'Senior'),
        ('LD', 'Lead'),
        ('MG', 'Manager')
    ]

    # Basic job fields
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    location = models.CharField(max_length=100)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    job_type = models.CharField(max_length=2, choices=JOB_TYPES)
    experience_level = models.CharField(max_length=2, choices=EXPERIENCE_LEVELS)
    skills_required = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class JobApplication(models.Model):
    # Simple status choices
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('R', 'Reviewing'),
        ('S', 'Shortlisted'),
        ('RJ', 'Rejected'),
        ('H', 'Hired')
    ]

    # Basic application fields
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    resume = models.ForeignKey('Resume', on_delete=models.CASCADE)
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='P')
    match_score = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.applicant.username}'s application for {self.job.title}"

class Resume(models.Model):
    # Basic resume fields
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(
        upload_to='resumes/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx'])]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ResumeAnalysis(models.Model):
    # Basic analysis fields
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE)
    skills = models.JSONField(default=list)
    experience = models.JSONField(default=list)
    education = models.JSONField(default=list)
    overall_score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Analysis for {self.resume.title}"

class ResumeFeedback(models.Model):
    # Basic feedback fields
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    feedback_type = models.CharField(max_length=50)
    message = models.TextField()
    severity = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.feedback_type} feedback for {self.resume.title}"

class SavedJob(models.Model):
    # Simple saved job model
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')

    def __str__(self):
        return f"{self.user.username} saved {self.job.title}"
