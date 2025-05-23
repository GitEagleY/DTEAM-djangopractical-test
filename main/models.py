from django.db import models

class ModelCV(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    bio = models.TextField()
    skills = models.JSONField()
    projects = models.JSONField()
    contacts = models.JSONField()

    def __str__(self):
        return f"{self.firstname} {self.lastname}"
