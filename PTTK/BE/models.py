from django.db import models

# Create your models here.
class User(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(unique=True, max_length=150)
    password = models.CharField(max_length=150)
class Editor(User):
    role = models.CharField(max_length=150)
    
class Post(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    total_like = models.IntegerField()
    created_at = models.DateTimeField()
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    status = models.BooleanField()
    