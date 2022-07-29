from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    ListView,
)

from .models import PythonTopic
from .forms import PythonTopicForm

from random import randint


class PythonTopicsListView(ListView):
    queryset = PythonTopic.objects.order_by("-last_edit")
    context_object_name = "python_topics"
    template_name = "catalogue/topics_list.html"


def create_python_topic_view(request):
    if request.method == 'POST':
        form = PythonTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            # commit=False tells Django that "Don't send this to database yet.
            # I have more things I want to do with it."

            topic.user = request.user # Set the user object here
            topic.save() # Now you can send it to DB

            return redirect("catalogue/topics_list.html")
    else:
        form = PythonTopicForm()
    return render(
        request,
        'catalogue/create_topic.html',
        {"form": form}
        )


def update_python_topic_view(request, pk=None):
    topic = get_object_or_404(PythonTopic, pk)
    if request.method == 'POST':
        form = PythonTopicForm(request.POST, instance=topic)
        if form.is_valid():
            topic.save()
            return redirect("catalogue/topics_list.html")
    else:
        form = PythonTopicForm(instance=topic)
    return render(
        request,
        'catalogue/update_topic.html',
        {"form": form,
        "topic": topic}
        )


def python_topic_detail_view(request, pk=None):
    python_topic = get_object_or_404(pk)
    return render(
        request,
        "catalogue/topic-detail.html",
        context={
            "python_topic": python_topic,
            }
        )


def python_topic_random_detail_view(request):
    # Grab random object
    num_topics = PythonTopic.objects.count()
    random_ind = randint(0, num_topics - 1)
    python_topic = get_object_or_404(random_ind)
    return render(
        request,
        "catalogue/topic-detail.html",
        context={
            "python_topic": python_topic,
            }
        )

