from django.contrib.auth.models import User
from django.db import models
# from django.db import models

# class TaskTable(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_set')
#     date = models.DateField(auto_now_add=True)
#     task_array = models.JSONField()
#     number_of_tasks = models.IntegerField()
#     remarks = models.TextField()
#     no_of_complete = models.IntegerField()

#     def __str__(self):
#         return f"{self.date} ----- {self.user.username}"










class TaskTable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='task_set')
    date = models.DateField(auto_now_add=True)
    taskName =models.CharField(max_length=100)
    taskTime=models.IntegerField()
    taskType=models.CharField(max_length=50)
    created_at = models.DateTimeField(blank=True,null=True)
    completed_at = models.DateTimeField(blank=True,null=True)
    is_checked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.date} ----- {self.user.username}"
    

class RemarksTable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='remark_set')
    date = models.DateField(auto_now_add=True)
    remarks = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.date} ----- {self.user.username}"