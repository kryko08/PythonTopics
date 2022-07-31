from django.contrib import admin
from .models import PythonTopic
from django.contrib.auth.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "id", "is_active")


class PythonTopicAdmin(admin.ModelAdmin):
    list_display = ("topic_name", "created", "user", "id")
admin.site.register(PythonTopic, PythonTopicAdmin)


