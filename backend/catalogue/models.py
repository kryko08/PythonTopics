from django.db import models
import os 

from django.utils import timezone

from django.contrib.auth.models import User

class PythonTopic(models.Model):

    def save_PythonTopic_file(self, filename):
        user = self.user.id
        path = f"topics/{user}/%d/%m/%Y/{filename}"
        return path

    created = models.DateTimeField()
    last_edit = models.DateField()
    topic_name = models.CharField(max_length=50)
    describtion = models.TextField(max_length=250)
    python_file = models.FileField(upload_to=save_PythonTopic_file)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.last_edit = timezone.now()
        return super(PythonTopic, self).save(*args, **kwargs)



