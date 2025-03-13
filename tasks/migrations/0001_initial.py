# Generated by Django 4.2.20 on 2025-03-13 06:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TaskName', models.CharField(max_length=200)),
                ('TaskDescription', models.TextField(blank=True)),
                ('TaskStatus', models.CharField(choices=[('pending', 'PENDING'), ('in_progress', 'IN_PROGRESS'), ('completed', 'COMPLETED'), ('cancelled', 'Cancelled')], default='pending', max_length=20)),
                ('CreatedAt', models.DateTimeField(auto_now_add=True)),
                ('UpdatedAt', models.DateTimeField(auto_now=True)),
                ('DueDate', models.DateTimeField(blank=True, null=True)),
                ('AssignedBy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_tasks', to=settings.AUTH_USER_MODEL)),
                ('AssignedTo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_tasks', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RateLimitRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('endpoint', models.CharField(max_length=255)),
                ('request_count', models.IntegerField(default=0)),
                ('window_start', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'endpoint', 'window_start')},
            },
        ),
    ]
