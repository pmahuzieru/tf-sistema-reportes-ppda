# Generated by Django 5.1.5 on 2025-03-22 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_customuser_body_alter_customuser_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='rut',
            field=models.CharField(default=111111111, max_length=12, unique=True),
            preserve_default=False,
        ),
    ]
