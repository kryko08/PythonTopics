from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
)

from .models import PythonTopic
from .forms import PythonTopicForm

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


class PythonTopicsDetailView(DetailView):
    pass


