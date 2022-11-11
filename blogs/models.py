from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Category(models.Model):
    pass
    name = models.CharField(max_length=50)

    class Meta:

        def __str__(self):
            return self.name


class Blog(models.Model):
    pass
    title = models.CharField("Blog title", max_length=75)
    description = models.CharField("Blog description", max_length=350)
    created_date = models.DateField("Created date")
    image_url = models.CharField("image url", max_length=2000)
    content = models.CharField("Blog content", max_length=10000)
    category = models.ManyToManyField(Category, verbose_name="Blog category")
    user = models.ForeignKey(User, related_name="blogs", on_delete=models.CASCADE, verbose_name="author")

    class Meta:

        def __str__(self):
            return self.title


class Comment(models.Model):
    pass
    
    blog = models.ForeignKey(Blog, related_name="comments", on_delete=models.CASCADE, verbose_name="blog")
    commenter = models.CharField("Commenter", max_length=100)
    comment_body = models.TextField("Comment")
    date_added = models.DateTimeField("Comment date", auto_now_add=True)

    class Meta:

        def __str__(self):
            return '%s - %s' % (self.blog.title, self.commenter)
