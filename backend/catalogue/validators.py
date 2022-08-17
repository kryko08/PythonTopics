from django.core.exceptions import ValidationError

def is_python_file_validator(fieldfile):
    import os
    filename, user_input = os.path.splitext(fieldfile.name)
    expected_filetype = ".py"
    error_message = f"File format invalid! Expected {expected_filetype}. Got instead {user_input}"
    if user_input != expected_filetype:
        raise ValidationError(error_message)
        