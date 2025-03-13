from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import TaskViewSet
from django.views.decorators.csrf import csrf_exempt 

#########   CSRF Protection Disabled for Testing 

router = DefaultRouter()
router.register(r'tasks',TaskViewSet,basename='task')

urlpatterns = [
    path('',include(router.urls)),
    path('token-auth/',csrf_exempt(obtain_auth_token),name='api_auth_token'),
]