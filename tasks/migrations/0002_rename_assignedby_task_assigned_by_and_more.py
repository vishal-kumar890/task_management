# Generated by Django 4.2.20 on 2025-03-13 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='AssignedBy',
            new_name='assigned_by',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='AssignedTo',
            new_name='assigned_to',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='CreatedAt',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='DueDate',
            new_name='due_date',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='TaskDescription',
            new_name='task_description',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='TaskName',
            new_name='task_name',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='UpdatedAt',
            new_name='updated_at',
        ),
        migrations.RemoveField(
            model_name='task',
            name='TaskStatus',
        ),
        migrations.AddField(
            model_name='task',
            name='task_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending', max_length=20),
        ),
    ]
