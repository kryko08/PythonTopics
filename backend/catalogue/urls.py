from django.urls import path, include

from .views import (
    PythonTopicsListView,
    create_python_topic_view,
    update_python_topic_view,
    python_topic_detail_view,
    python_topic_random_detail_view,
    UserTopicsListView
    )


urlpatterns = [
    path('topics/', include([
        path('', PythonTopicsListView.as_view(), name="topic-list"),
        path('create/', create_python_topic_view, name="topic-create"),
        path('<int:pk>/detail/', python_topic_detail_view, name="topic-detail"),
        path('<int:pk>/update/', update_python_topic_view, name="topic-update"),
        path("random_topic/", python_topic_random_detail_view, name="topic-random"),
        path('users/<int:pk>/', UserTopicsListView.as_view(), name="user-topic-list")
    ])),
]
