from django.contrib.auth.models import User
from django.db import models

class Contact(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.FileField(blank=True, null=True)

    def __str__(self):
        return self.user.username

    def fullname(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Message(models.Model):
    source = models.ForeignKey(Contact, related_name="source", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    picture = models.FileField(blank=True, null=True)
    destination = models.ForeignKey(Contact, related_name="destination", on_delete=models.CASCADE)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.source.user.username} - {self.destination.user.username}'
