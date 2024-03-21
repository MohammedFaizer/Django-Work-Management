from django.contrib.auth.models import User
from django.db import models

class TaskTable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    task_array = models.JSONField()
    number_of_tasks = models.IntegerField()
    remarks = models.TextField()
    no_of_complete=models.IntegerField()

    def __str__(self):
        return f"{self.date} ----- {self.user.username}"
