from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    ListView,
)

from .models import PythonTopic
from .forms import PythonTopicForm

from random import randint

from django.http import HttpResponseRedirect
from django.urls import reverse


class PythonTopicsListView(ListView):
    queryset = PythonTopic.objects.order_by("-last_edit")
    context_object_name = "python_topics"
    template_name = "catalogue/topics_list.html"


def create_python_topic_view(request):
    if request.method == 'POST':
        form = PythonTopicForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data["python_file"]
            topic = form.cleaned_data["topic_name"]
            describtion = form.cleaned_data["describtion"]
            user = request.user 

            # Create object 
            obj = PythonTopic(topic_name=topic, describtion=describtion, python_file=file, user=user)
            obj.save() # Save object

            return HttpResponseRedirect(reverse('topic-detail', kwargs={'pk': obj.id}))
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
    python_topic = get_object_or_404(PythonTopic, pk=pk)
    return render(
        request,
        "catalogue/topic_detail.html",
        context={
            "python_topic": python_topic,
            }
        )


def python_topic_random_detail_view(request):
    # Grab random object
    topic_ids = PythonTopic.objects.values_list("id", flat=True)
    num_topic = len(topic_ids)
    ind = randint(0, num_topic-1)
    random_id = topic_ids[ind]
    python_topic = get_object_or_404(PythonTopic, pk=random_id)
    return render(
        request,
        "catalogue/topic_detail.html",
        context={
            "python_topic": python_topic,
            }
        )
