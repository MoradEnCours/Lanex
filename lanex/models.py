from django.db import models


class Language(models.Model):
    name = models.CharField(max_length=128, unique=True)
    picture = models.ImageField(upload_to='languages', default='languages/lan.jpg')

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    username = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=64, unique=True)
    email = models.CharField(max_length=64, unique=True)
    pageURL = models.CharField(max_length=128, unique=True)
    language = models.CharField(max_length=128, unique=True)
    location = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.username
        
class LanguageRequest(models.Model):
    title = models.CharField(max_length=128)
    views = models.IntegerField(default=0)
    request_id = models.CharField(max_length=128,primary_key=True)
    time = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=128, unique=True)
    sessionID = models.IntegerField(default=0)

    def __str__(self):
        return self.sessionID
