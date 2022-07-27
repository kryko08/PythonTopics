from dataclasses import fields
from django.forms import ModelForm
from .models import PythonTopic

class PythonTopicForm(ModelForm):
    class Meta:
        model = PythonTopic
        fields = [
            "topic_name",
            "describtion",
            "python_file",
        ]
