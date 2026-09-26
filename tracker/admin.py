from django.contrib import admin
from .models import Task, SubTask

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_completed', 'is_default', 'created_at')
    list_filter = ('category', 'is_completed', 'is_default')
    search_fields = ('title',)

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'is_completed')
    list_filter = ('is_completed',)