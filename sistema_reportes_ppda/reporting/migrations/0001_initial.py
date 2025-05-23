# Generated by Django 5.1.5 on 2025-03-23 15:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('management', '0010_environmentalplan_short_name_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProgressReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('publication_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_progress_reports', to=settings.AUTH_USER_MODEL)),
                ('environmental_plan', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='progress_reports', to='management.environmentalplan')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='updated_progress_reports', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
