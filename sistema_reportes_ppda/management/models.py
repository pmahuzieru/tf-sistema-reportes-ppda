from django.db import models
from accounts.models import CustomUser

class EnvironmentalPlan(models.Model):
    PLAN_TYPE_CHOICES = [  # https://ppda.mma.gob.cl/
        ("PPA", "Plan de Prevención Atmosférica (PPA)"),
        ("PDA", "Plan de Descontaminación Atmosférica (PDA)"),
        ("PPDA", "Plan de Prevención y Descontaminación Atmosférica (PPDA)")
    ]
    
    name = models.CharField(max_length=200, null=False, blank=False)
    type = models.CharField(max_length=4, choices=PLAN_TYPE_CHOICES, default="PPDA", null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="created_plans", null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='updated_plans', null=True, blank=True)
    
    def __str__(self):
        return self.name


class Measure(models.Model):
    MEASURE_TYPE_CHOICES = [ 
        ('NA', "No Aplica"),
        ('PP', "Politica Publica"),
        ('EyD', "Educacion y Difusion"),
        ('E', "Estudios"),
        ('O', "Otra")
    ]

    reference_PDA = models.ForeignKey(EnvironmentalPlan, on_delete=models.PROTECT, related_name='measures', null=False, blank=False)
    measure_type = models.CharField(max_length=4, choices=MEASURE_TYPE_CHOICES, default=None, blank=True)
    short_name = models.CharField(max_length=500, null=False, blank=False)
    indicator = models.CharField(max_length=500, null=False, blank=False)
    calculation_formula = models.CharField(max_length=500, null=False, blank=False)
    reporting_frequency = models.CharField(max_length=50, null=False, blank=False)
    verification_methods = models.CharField(max_length=500, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name="created_measures", null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='updated_measures', null=True, blank=True)
    is_regulatory = models.BooleanField(default=True)

    def __str__(self):
        return self.short_name