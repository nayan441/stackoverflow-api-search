from django.db import models
from django.contrib.sessions.models import Session

class SearchRecord(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    # any other relevant data