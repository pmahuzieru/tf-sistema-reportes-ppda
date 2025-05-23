# Generated by Django 5.1.5 on 2025-04-04 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0010_environmentalplan_short_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='measure',
            name='value_type',
            field=models.CharField(choices=[('boolean', 'Boolean'), ('integer', 'Integer'), ('decimal', 'Decimal'), ('proportion', 'Proportion'), ('text', 'Text')], default='text', max_length=10),
            preserve_default=False,
        ),
    ]
