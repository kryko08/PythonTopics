from django.forms import ModelForm
from django import forms

from django.contrib.auth.forms import (
    UserCreationForm,
)
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

from .validators import is_python_file_validator
from .models import PythonTopic

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


class CustomUserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2"
        ]