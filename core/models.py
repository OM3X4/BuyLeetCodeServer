from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    name = models.CharField(max_length=100)

class Tag(models.Model):
    name = models.CharField(max_length=100)

# Create your models here.
class Question(models.Model):
    class Difficulty(models.TextChoices):
        EASY = 'E', 'Easy',
        MEDIUM = 'M', 'Medium',
        HARD = 'H', 'Hard'


    title = models.CharField(max_length=200)
    difficulty = models.CharField(max_length=50 , choices=Difficulty.choices)
    url = models.URLField()
    acceptanceRate = models.FloatField()
    companies = models.ManyToManyField(Company, related_name='questions')
    solution = models.TextField()
    explanation = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='questions')

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User , on_delete=models.CASCADE)  # Assuming you have a User model or similar for authors
    upvotes = models.IntegerField(default=0)
    upvoters = models.ManyToManyField(User, related_name='upvoted_posts', blank=True)

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming you have a User model or similar for authors
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)