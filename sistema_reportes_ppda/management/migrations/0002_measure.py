# Generated by Django 5.1.5 on 2025-02-02 21:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Measure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('measure_type', models.CharField(blank=True, choices=[('NA', 'No Aplica'), ('PP', 'Politica Publica'), ('EyD', 'Educacion y Difusion'), ('E', 'Estudios'), ('O', 'Otra')], default=None, max_length=4)),
                ('short_name', models.CharField(max_length=500)),
                ('indicator', models.CharField(max_length=500)),
                ('calculation_formula', models.CharField(max_length=500)),
                ('reporting_frequency', models.CharField(max_length=50)),
                ('verification_methods', models.CharField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_regulatory', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_measures', to=settings.AUTH_USER_MODEL)),
                ('reference_PDA', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='measures', to='management.environmentalplan')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='updated_measures', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
