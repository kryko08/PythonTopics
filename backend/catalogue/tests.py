from unittest import skipIf
from django.urls import reverse
from django.test import (
    TestCase,
    Client,
    SimpleTestCase
)

from .models import PythonTopic
import random
from django.contrib.auth.models import User

# Testing Views

class UserAccessTestCase(TestCase):

    def setUp(self):
        # Logged client
        user = User.objects.create_user(
            username='test_client',
            email='test@gmail.com',
            password='test_clienttest_client'
        )
        self.logged_client = Client()
        self.logged_client.login(username='test_client',password='test_clienttest_client')

        # admin
        super_user = User.objects.create_user(
            username='admin',
            email='admin@gmail.com',
            password='adminadmin',
            is_superuser=True
        )
        self.admin_client = Client()
        self.admin_client.login(username="admin",password="adminadmin")

        # Anonymous client
        self.anonymous_client = Client()

        # Create Python topic owned by admin
        admin = User.objects.filter(username="admin")[0]
        self.admin_topic = PythonTopic.objects.create(
            user=admin,
            topic_name="test_topic",
            describtion="test_describtion"
        )

        # Create python topic owned by other user
        ordinary_user = User.objects.filter(username="test_client")[0]
        self.topic = PythonTopic.objects.create(
            user=ordinary_user,
            topic_name="test_topic",
            describtion="test_describtion"
        )

    # User has to be logged in to view topic detail
    def test_anonymous_topic_detail_view(self):
        topic_id = self.admin_topic.id
        response = self.anonymous_client.get(reverse("topic-detail", kwargs={"pk":topic_id})).status_code
        # Anonymous user is redirected to login page
        expected_status_code = 302
        self.assertEqual(
            response,
            expected_status_code,
            f"status codes don't match! Got: {response}, expected: {expected_status_code}")
        

    # Only owner can update their topic 
    def test_not_owner_topic_update_view(self):
        topic_id = self.admin_topic.id
        response = self.logged_client.get(reverse("topic-update", kwargs={"pk":topic_id})).status_code
        forbidden_status_code = 403
        # Only owner and admin can edit their post
        self.assertEqual(
            response,
            forbidden_status_code,
            f"status codes don't match! Got: {response}, expected: {forbidden_status_code}"
        )

    # Admin can request any topic
    def test_admin_detail_view_access(self):
        topic_id = self.topic.id
        response = self.logged_client.get(reverse("topic-update", kwargs={"pk":topic_id})).status_code
        ok_status_code = 200
        self.assertEqual(
            response,
            ok_status_code,
            f"status codes don't match! Got: {response}, expected: {ok_status_code}"
        )


class PostTopicCookieTestCase(TestCase):

    def setUp(self):
        # Logged client
        user = User.objects.create_user(
            username='test_client',
            email='test@gmail.com',
            password='test_clienttest_client'
        )
        self.logged_client = Client()
        self.logged_client.login(username='test_client',password='test_clienttest_client')

    @skipIf(True, "This test is not ready yes")
    def test_blbost(self):
        pass

