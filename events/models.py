from django.db import models
from accounts.models import User

class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=100)
    tickets_number = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class CreateEvent(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Create Events'