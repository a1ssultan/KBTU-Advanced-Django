from rest_framework import serializers
from .models import Job, JobApplication, JobMatch, SavedJob, Resume, ResumeAnalysis, ResumeFeedback
from django.contrib.auth.models import User
from resume_processing.serializers import ResumeSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class JobSerializer(serializers.ModelSerializer):
    recruiter = UserSerializer(read_only=True)
    applications_count = serializers.SerializerMethodField()
    match_score = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def get_applications_count(self, obj):
        return obj.applications.count()

    def get_match_score(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                match = JobMatch.objects.get(job=obj, resume__user=request.user)
                return match.match_score
            except JobMatch.DoesNotExist:
                return None
        return None

class JobApplicationSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)
    applicant = UserSerializer(read_only=True)
    resume = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = JobApplication
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'status', 'match_score')

class JobMatchSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)
    resume = ResumeSerializer(read_only=True)

    class Meta:
        model = JobMatch
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class SavedJobSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = SavedJob
        fields = '__all__'
        read_only_fields = ('created_at',)

class JobApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['job', 'resume', 'cover_letter']

    def validate(self, data):
        user = self.context['request'].user
        job = data['job']
        resume = data['resume']

        if resume.user != user:
            raise serializers.ValidationError("You can only apply with your own resume")

        if JobApplication.objects.filter(job=job, applicant=user).exists():
            raise serializers.ValidationError("You have already applied for this job")

        return data

class JobSearchSerializer(serializers.Serializer):
    title = serializers.CharField(required=False)
    location = serializers.CharField(required=False)
    job_type = serializers.ChoiceField(choices=Job.JOB_TYPES, required=False)
    experience_level = serializers.ChoiceField(choices=Job.EXPERIENCE_LEVELS, required=False)
    skills = serializers.ListField(child=serializers.CharField(), required=False)
    salary_min = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    salary_max = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)

class ResumeAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeAnalysis
        fields = ['skills', 'experience', 'education', 'overall_score', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class ResumeFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeFeedback
        fields = ['feedback_type', 'message', 'severity', 'created_at']
        read_only_fields = ['created_at'] 