from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Blog(models.Model):
    title = models.CharField(max_length=75)
    description = models.CharField(max_length=350)
    created_date = models.DateField()
    image_url = models.CharField(max_length=2000)
    content = models.CharField(max_length=10000)
    category = models.ManyToManyField(Category)
    user = models.ForeignKey(User, related_name="blogs", on_delete=models.CASCADE)
      
    def __str__(self):
        return self.title

class Comment(models.Model):
    blog = models.ForeignKey(Blog, related_name="comments", on_delete=models.CASCADE)
    commenter = models.CharField(max_length=100)
    comment_body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.blog.title, self.commenter)
