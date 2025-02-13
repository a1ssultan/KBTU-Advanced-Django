from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path

from task_management import settings
from .views import UserViewSet, ProjectViewSet, CategoryViewSet, PriorityViewSet, TaskViewSet, contact_view, \
    success_view, create_cv, cv_list, share_cv_email
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'priorities', PriorityViewSet)
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('contact/', contact_view, name='contact'),
    path('success/', success_view, name='success_page'),
    path('create_cv/', create_cv, name='create_cv'),
    path('cv/', cv_list, name='cv_list'),
    path('share/email/<int:cv_id>/', share_cv_email, name='share_cv_email'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += router.urls
