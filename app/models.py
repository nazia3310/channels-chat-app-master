from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Message(models.Model):
    msg = models.CharField(max_length=100)
    timedate = models.DateTimeField(auto_now=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")

    def __str__(self):
        return self.msg