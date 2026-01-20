import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length = 200)
    pub_time = models.DateTimeField("publish time")

    def __str__(self): 
        return self.question_text

    @admin.display(
            boolean=True,
            ordering="pub_time",
            description="Published Today?"
            )
    def was_published_today(self):
        now = timezone.now()
        return ( self.pub_time <= now and self.pub_time >= (now - datetime.timedelta(days=1)) )

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length = 200)
    votes = models.IntegerField(default= 0)

    def __str__(self):
        return self.choice_text
