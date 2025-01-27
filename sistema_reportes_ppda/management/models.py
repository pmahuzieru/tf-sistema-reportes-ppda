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
