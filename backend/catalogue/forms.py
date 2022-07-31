from django.forms import ModelForm, Textarea
from django import forms
from .models import PythonTopic

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

from .validators import is_python_file_validator

class PythonTopicForm(ModelForm):
    python_file = forms.FileField(validators=[is_python_file_validator])
    class Meta:
        model = PythonTopic
        fields = [
            "topic_name",
            "describtion",
            "python_file",
        ]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "topic_name",
            "describtion",
            "python_file",
            Submit('submit', 'Submit', css_class='button white'),
        )
