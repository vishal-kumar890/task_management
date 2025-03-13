from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import TestCase, override_settings
from unittest.mock import patch, MagicMock
from rest_framework import status
from rest_framework.test import APIClient

from tasks.views import RateLimitedViewMixin

class RateLimitingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            email='test@example.com', 
            password='testpass123'
        )
        
        # self.client = APIClient()
        # self.client.force_authenticate(user=self.user)

        # Just for testing purpose i have used MagicMock instead of APIClient
        # Create a mock request
        self.request = MagicMock()
        self.request.user = self.user
        self.mixin = RateLimitedViewMixin()
        cache.clear()
    
    @override_settings(RATE_LIMIT_REQUESTS=5, RATE_LIMIT_WINDOW=60)
    def test_rate_limit_under_limit(self):
        # This will test request is under allowed limit or not
        for _ in range(4):
            result = self.mixin.check_rate_limit(self.request, 'TestView')
            self.assertTrue(result)
    
    @override_settings(RATE_LIMIT_REQUESTS=5, RATE_LIMIT_WINDOW=60)
    def test_rate_limit_exceeded(self):
        # This will check the request block after limit exceed
        for _ in range(5):
            self.mixin.check_rate_limit(self.request, 'TestView')
        
        result = self.mixin.check_rate_limit(self.request, 'TestView')
        self.assertFalse(result)
    

        