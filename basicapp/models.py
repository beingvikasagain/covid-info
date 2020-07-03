from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

# Create your models here.

class UserProfileInfoModel(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    userportfoliosite = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    author = models.ForeignKey("auth.User",on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail',kwargs={'pk':self.pk})

    def publish(self):
        self.published_date=timezone.now()
        self.save()

    def approve_comment(self):
        return self.comments.filter(approved_comment=True)


class Comment(models.Model):

    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    email = models.EmailField()
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('post_detail',kwargs={'pk':self.post.pk})

    def __str__(self):
        return self.text

    def approve(self):
        self.approved_comment=True
        self.save()
