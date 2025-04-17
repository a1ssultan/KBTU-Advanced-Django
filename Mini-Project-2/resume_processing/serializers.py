from rest_framework import serializers
from .models import Resume, ResumeAnalysis, Skill, Experience, Education
from user_management.serializers import UserSerializer

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class ResumeAnalysisSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    experiences = ExperienceSerializer(many=True, read_only=True)
    educations = EducationSerializer(many=True, read_only=True)

    class Meta:
        model = ResumeAnalysis
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class ResumeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    analysis = ResumeAnalysisSerializer(read_only=True)
    experiences = ExperienceSerializer(many=True, read_only=True)
    educations = EducationSerializer(many=True, read_only=True)

    class Meta:
        model = Resume
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'status')

class ResumeUploadSerializer(serializers.ModelSerializer):
    file = serializers.FileField()

    class Meta:
        model = Resume
        fields = ('file',)

    def create(self, validated_data):
        user = self.context['request'].user
        file = validated_data['file']
        
        resume = Resume.objects.create(
            user=user,
            file=file,
            original_filename=file.name,
            file_type=file.name.split('.')[-1].lower()
        )
        
        return resume

class ResumeFeedbackSerializer(serializers.Serializer):
    resume_id = serializers.IntegerField()
    feedback = serializers.CharField()
    score = serializers.FloatField(min_value=0, max_value=100)

    def validate_resume_id(self, value):
        try:
            Resume.objects.get(id=value)
        except Resume.DoesNotExist:
            raise serializers.ValidationError("Resume not found")
        return value 