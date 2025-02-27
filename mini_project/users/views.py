from rest_framework import viewsets, generics
from .models import User
from .permissions import IsAdmin
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny


# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "list":
            return [IsAdmin()]
        elif self.action in ["destroy"]:
            return [IsAdmin()]
        elif self.action in ["retrieve", "update", "partial_update"]:
            return [IsAuthenticated()]
        elif self.action == "create":
            return [AllowAny()]
        return [AllowAny()]


class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []
