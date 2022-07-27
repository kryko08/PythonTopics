from django.urls import path, include

from .views import (
    PythonTopicsListView,
    create_python_topic_view,
    PythonTopicsDetailView,
    update_python_topic_view,
    )


urlpatterns = [
    path('topics/', include([
        path('', PythonTopicsListView.as_view(), name="topics-list"),
        path('create/', create_python_topic_view, name="create-topic"),
        path('<int:pk>/detail', PythonTopicsDetailView.as_view(), name="topic-detail"),
        path('<int:pk>/update', update_python_topic_view, name="topic-update"),
    ])),
]
