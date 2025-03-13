from django.contrib import admin
from .models import Task

# Register your models here.
@admin.register(Task)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','task_name','task_status','created_at')
    search_fields = ('id,''task_name','task_status')
    list_filter = ('task_status',)
    ordering = ('-created_at',)

