# Generated by Django 5.1.5 on 2025-02-05 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='rut',
            field=models.CharField(default='12.486.154-3', max_length=12, unique=True),
            preserve_default=False,
        ),
    ]
