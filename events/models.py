from django.db import models

# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField()
    total_participants = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.title