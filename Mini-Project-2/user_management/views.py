from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import secrets
from .models import JobSeekerProfile, RecruiterProfile, EmailVerification
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    JobSeekerProfileSerializer,
    RecruiterProfileSerializer,
    EmailVerificationSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer
)

User = get_user_model()

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        # Create profile based on role
        if user.role == User.Role.JOB_SEEKER:
            JobSeekerProfile.objects.create(user=user)
        elif user.role == User.Role.RECRUITER:
            RecruiterProfile.objects.create(user=user)
        
        # Create email verification token
        token = secrets.token_urlsafe(32)
        EmailVerification.objects.create(
            user=user,
            token=token,
            expires_at=timezone.now() + timedelta(days=1)
        )
        # TODO: Send verification email

class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        user = self.request.user
        if user.role == User.Role.JOB_SEEKER:
            return JobSeekerProfileSerializer
        elif user.role == User.Role.RECRUITER:
            return RecruiterProfileSerializer
        return UserSerializer

    def get_object(self):
        user = self.request.user
        if user.role == User.Role.JOB_SEEKER:
            return user.job_seeker_profile
        elif user.role == User.Role.RECRUITER:
            return user.recruiter_profile
        return user

class EmailVerificationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get('token')
        try:
            verification = EmailVerification.objects.get(
                token=token,
                expires_at__gt=timezone.now()
            )
            verification.user.is_email_verified = True
            verification.user.save()
            verification.delete()
            return Response({'message': 'Email verified successfully'})
        except EmailVerification.DoesNotExist:
            return Response(
                {'error': 'Invalid or expired token'},
                status=status.HTTP_400_BAD_REQUEST
            )

class PasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                token = secrets.token_urlsafe(32)
                EmailVerification.objects.create(
                    user=user,
                    token=token,
                    expires_at=timezone.now() + timedelta(hours=1)
                )
                # TODO: Send password reset email
                return Response({'message': 'Password reset email sent'})
            except User.DoesNotExist:
                return Response(
                    {'error': 'User not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            try:
                verification = EmailVerification.objects.get(
                    token=token,
                    expires_at__gt=timezone.now()
                )
                user = verification.user
                user.set_password(serializer.validated_data['password'])
                user.save()
                verification.delete()
                return Response({'message': 'Password reset successful'})
            except EmailVerification.DoesNotExist:
                return Response(
                    {'error': 'Invalid or expired token'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
