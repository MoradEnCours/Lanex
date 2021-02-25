from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Language(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
    picture = models.ImageField(upload_to='languages', default='languages/lan.jpg')
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Language, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class LanguageRequest(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)
    ### Je dois repenser ceci-dessus
    #request_id = models.CharField(max_length=128,primary_key=True)
    #time = models.DateTimeField(auto_now=True)
    #location = models.CharField(max_length=128, unique=True)
    #sessionID = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_images', default='profile_images/default.jpg')
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username

        


