from django.db import models

# Create your models here.

class Post(models.Model) :
        title = models.CharField(max_length=50)
        content = models.TextField()
        updated_at = models.models.DateTimeField(auto_now=True)