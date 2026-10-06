from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    CATEGORY_CHOICES = [
        ('study', 'Study & Focus'),
        ('mental', 'Mental Wellness'),
        ('physical', 'Physical Wellness'),
        ('food', 'Food & Hydration'),
        ('custom', 'Personal Goal'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='custom')
    is_completed = models.BooleanField(default=False)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"

class SubTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False) 
    due_date = models.DateField(null=True, blank=True)

class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Goal(models.Model):
    title = models.CharField(max_length=200)
    target_date = models.DateField(null=True, blank=True)
    progress = models.IntegerField(default=0)  # 0 to 100%

    def __str__(self):
        return self.title