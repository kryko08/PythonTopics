from django.core.exceptions import ValidationError

def is_python_file_validator(fieldfile):
    import os
    filename, user_input = os.path.splitext(fieldfile.name)
    error_message = "File format invalid! Expected %(expected_file_format)s. Got instead %(got_instead)s"
    expected_filetype = ".py"
    error_dict = {
        "expected_file_format": expected_filetype,
        "got_instead": user_input
    }

    if user_input != expected_filetype:
        raise ValidationError(error_message, error_dict)
        