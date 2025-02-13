from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
import logging
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from rest_framework.viewsets import ModelViewSet

from task_management import settings
from .models import User, Project, Category, Priority, Task, CV
from .permissions import IsAdmin, IsManager, IsEmployee
from .serializers import UserSerializer, ProjectSerializer, CategorySerializer, PrioritySerializer, TaskSerializer

from .forms import ContactForm, CVForm

logger = logging.getLogger(__name__)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = [IsAdmin]


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    permission_classes = [IsManager]


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class PriorityViewSet(ModelViewSet):
    queryset = Priority.objects.all()
    serializer_class = PrioritySerializer


class TaskViewSet(ModelViewSet):
    permission_classes = [IsEmployee]

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        logger.info("Creating a new task")
        serializer.save()

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['project', 'priority', 'category']
    search_fields = ['title', 'description']


def contact_view(request):
    if request.method == "POST":

        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()  # Saves directly to the database

            return redirect('success_page')

    else:

        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


def success_view(request):
    return render(request, 'success.html')


def create_cv(request):

    if request.method == "POST":

        form = CVForm(request.POST, request.FILES)  # Handle file uploads

        if form.is_valid():

            form.save()

            return redirect('cv_list')  # Redirect to CV listing page

    else:

        form = CVForm()

    return render(request, 'cv_form.html', {'form': form})


def cv_list(request):
    cvs = CV.objects.all()
    return render(request, 'cv_list.html', {'cvs': cvs})


def share_cv_email(request, cv_id):
    cv = get_object_or_404(CV, id=cv_id)

    recipient_email = request.POST.get('email')

    if recipient_email:

        subject = f"{cv.name}'s CV"

        message = f"Check out {cv.name}'s CV at {request.build_absolute_uri(cv.profile_picture.url)}"

        sender_email = settings.EMAIL_HOST_USER

        send_mail(subject, message, sender_email, [recipient_email])

        messages.success(request, "CV shared successfully via email.")

    else:

        messages.error(request, "Please provide a valid email.")

    return redirect('cv_list')
