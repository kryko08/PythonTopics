from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import Http404, HttpResponseRedirect
from django.views.generic import (
    ListView,
)
from django.core.exceptions import PermissionDenied


from .models import PythonTopic
from .forms import PythonTopicForm, CustomUserRegistrationForm

from Topics.settings import MEDIA_ROOT

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

import os
import sys
import importlib.util
import inspect
import subprocess
from random import randint
from ast import mod
import operator


class PythonTopicsListView(ListView):
    queryset = PythonTopic.objects.order_by("-last_edit")
    context_object_name = "python_topics"
    template_name = "catalogue/topics_list.html"


@login_required()
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


@login_required()
def update_python_topic_view(request, pk=None):
    # Check if user is owner or admin (admin can edit any posts) 
    topic = get_object_or_404(PythonTopic, pk=pk)
    if request.user != topic.user and not request.user.is_superuser:
            raise PermissionDenied

    # Handle update
    if request.method == 'POST':
        form = PythonTopicForm(request.POST, request.FILES, instance=topic)
        if form.is_valid():
            file = form.cleaned_data["python_file"]
            topic_name = form.cleaned_data["topic_name"]
            describtion = form.cleaned_data["describtion"]
            # Override data
            # PythonTopic.objects.filter(pk=pk).update(topic_name=topic_name, describtion=describtion, python_file=file)
            topic.topic_name = topic_name
            topic.python_file = file
            topic.describtion = describtion
            topic.save()
            return HttpResponseRedirect(
                reverse('topic-detail', kwargs={'pk': topic.id}))
    else:
        form = PythonTopicForm(instance=topic)

    return render(
        request,
        'catalogue/update_topic.html',
        {"form": form,
        "topic": topic}
        )


@login_required()
def python_topic_detail_view(request, pk=None):
    # Grab detail object
    python_topic = get_object_or_404(PythonTopic, pk=pk)

    # Read code from .py file 
    file_path = python_topic.python_file.path
    # Get module name
    head, module_name = os.path.split(file_path)
    module_name, ext = os.path.splitext(module_name)

    # add file to sys
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    source_code = inspect.getsourcelines(module)
    terminal = 0

    return render(
        request,
        "catalogue/topic_detail.html",
        context={
            "python_topic": python_topic,
            "code": source_code,
            "terminal": terminal,

            }
        )


def python_topic_random_detail_view(request):
    # Grab random object
    topic_ids = PythonTopic.objects.values_list("id", flat=True)
    num_topic = len(topic_ids)
    # No published topics condition
    if num_topic == 0:
        raise Http404("No topics were published yet.")

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


def sign_up(request):
    if request.method == "POST":
        print("tady")
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/topics')
    else:
        print("here")
        form = CustomUserRegistrationForm()

    return render(request, "registration/sign_up.html", {
        "form": form
    })
    
