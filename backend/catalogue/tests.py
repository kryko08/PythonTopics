from django.urls import reverse

from unittest import skipIf
from django.test import (
    TestCase,
    Client,
    override_settings
)

from django.core.exceptions import ValidationError

from .models import PythonTopic
from .forms import PythonTopicForm

from django.contrib.auth.models import User

from Topics.settings import (
    BASE_DIR,
    MEDIA_ROOT,
    TEST_MEDIA_ROOT
)

import shutil, os

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


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class PostTopicTestCase(TestCase):

    def setUp(self):
        # Logged client
        user = User.objects.create_user(
            username='test_client',
            email='test@gmail.com',
            password='test_clienttest_client'
        )
        self.logged_client = Client()
        self.logged_client.login(username='test_client',password='test_clienttest_client')

    def test_database_not_empty_after_post(self):
        user = User.objects.filter(username="test_client")[0]
        with open(f"{BASE_DIR}/test_utils/hello.py", "r") as f:
            self.logged_client.post("/topics/create/",
            {"topic_name": "test", "describtion": "test describtion", "python_file": f, "user":user}
            )
        # Check the database
        topic = PythonTopic.objects.filter(topic_name="test")[0]
        num_topics = PythonTopic.objects.count()
        self.assertGreater(num_topics, 0, f"Database contains {num_topics} topics, Expected 1")

    @skipIf(True, "test not ready yet")
    def test_topic_post_cookie(self):
        pass

    def test_form_invalid_file_type(self):
        user = User.objects.filter(username="test_client")[0]
        with open(f"{BASE_DIR}/test_utils/not-a-python-file.rtf", "r") as f:
            response = self.logged_client.post("/topics/create/",
            {"topic_name": "test", "describtion": "test describtion", "python_file": f, "user":user}
            )
        expected_error_message = "File format invalid! Expected .py. Got instead .rtf"
        self.assertFormError(response, form="form",field="python_file", errors=[expected_error_message])

    def tearDown(self):
        folder = f"{TEST_MEDIA_ROOT}"
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
        return super().tearDown()
