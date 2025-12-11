from django.db import models
import uuid
# Create your models here.

#task
class Tasks(models.Model):
    user_name = models.CharField(max_length=150, db_index=True)
    task_name=models.CharField(max_length=225)
    task_status=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)

    owner_id = models.UUIDField(default=uuid.uuid4,db_index=True)
    
    def __str__(self):
        return self.task_name