from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Project(models.Model):
    project_id = models.CharField(max_length=50)
    project_name = models.CharField(max_length=50)
    objective = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    no_of_programmer = models.IntegerField(default=0)
    complete_part = models.IntegerField(default=0)

    def __str__(self):
        return str(self.project_id)


def user_directory_path(instance, filename):
    return 'documents/{0}/{1}/{2}'.format(instance.programmer_id, instance.project_id, filename)


class Work(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True)
    programmer_id = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.TextField()
    file = models.FileField(upload_to=user_directory_path)
    status = models.BooleanField(default=False)
    start_time = models.IntegerField(default=0)
    end_time = models.IntegerField(default=0)

    def __str__(self):
        return str(self.project_id)