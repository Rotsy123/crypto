from django.db import models

class RegisteredUser(models.Model):
    username = models.CharField(max_length=100, unique=True)
    public_key = models.TextField()

    def __str__(self):
        return self.username
