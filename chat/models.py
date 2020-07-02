from django.contrib.auth.models import User
from django.db import models

class Contact(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.user.username

    def fullname(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def initial(self):
        return self.user.username[0].upper()

class Message(models.Model):
    source = models.ForeignKey(User, related_name="source", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(blank=True, auto_now_add=True)
    file = models.FileField(blank=True, null=True)
    destination = models.ForeignKey(User, related_name="destination", on_delete=models.CASCADE)
    read = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return f'{self.content} : {self.source.user.username} - {self.destination.user.username}'
