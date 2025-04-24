from django.db import models


class EnvironmentalPlan(models.Model):
    """
    Represents an instance of an "Plan de Prevención y Descontaminación Ambiental" in
    the system. It's used as the main reference to it, with its main attributes being
    related through the other models.
    """
    
    PLAN_TYPE_CHOICES = [  # https://ppda.mma.gob.cl/
        ("PPA", "Plan de Prevención Atmosférica (PPA)"),
        ("PDA", "Plan de Descontaminación Atmosférica (PDA)"),
        ("PPDA", "Plan de Prevención y Descontaminación Atmosférica (PPDA)"),
    ]

    name = models.CharField(max_length=200, null=False, blank=False)
    short_name = models.CharField(max_length=50, null=False, blank=False)
    type = models.CharField(
        max_length=4, choices=PLAN_TYPE_CHOICES, default="PPDA", null=False, blank=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.PROTECT,
        related_name="created_plans",
        null=False,
        blank=False,
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.PROTECT,
        related_name="updated_plans",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.short_name


class Measure(models.Model):
    """
    Represents an environmental measure ("medida"), which is a set of defined tasks/conditions
    that must be completed by the assigned Sectorial Bodies. A set of measures compose
    an Environmental Plan (PPDA).
    """
    
    MEASURE_TYPE_CHOICES = [
        ("R", "Regulación"),
        ("FAE", "Fomento de actividades económicas"),
        ("BIG", "Beneficios interés general"),
        ("E", "Estudios"),
        ("ED", "Educación y difusión"),
        ("PP", "Política pública"),
    ]
    
    MEASURE_VALUE_TYPES = [
        ('boolean', 'Boolean'),
        ('integer', 'Integer'),
        ('decimal', 'Decimal'),
        ('proportion', 'Proportion'),
        ('text', 'Text')
    ]

    reference_PDA = models.ForeignKey(
        EnvironmentalPlan,
        on_delete=models.PROTECT,
        related_name="measures",
        null=False,
        blank=False,
    )
    measure_type = models.CharField(
        max_length=4, choices=MEASURE_TYPE_CHOICES, default=None, blank=True
    )
    short_name = models.CharField(max_length=500, null=False, blank=False)
    indicator = models.CharField(max_length=500, null=False, blank=False)
    calculation_formula = models.CharField(max_length=500, null=False, blank=False)
    value_type = models.CharField(max_length=10, choices=MEASURE_VALUE_TYPES, null=False, blank=False)
    reporting_frequency = models.CharField(max_length=50, null=False, blank=False)
    verification_methods = models.CharField(max_length=500, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.PROTECT,
        related_name="created_measures",
        null=False,
        blank=False,
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.PROTECT,
        related_name="updated_measures",
        null=True,
        blank=True,
    )
    is_regulatory = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.reference_PDA.short_name} - {self.short_name}"
    
    def has_reports(self) -> bool:
        return self.measure_reports.exists()
    
    def get_latest_report(self):
        return self.measure_reports.order_by('-created_at').first()


class MeasureReport(models.Model):
    """
    Represents the result of the reporting on the current value of a measure's
    indicator. Multiple reports are allowed on each measure, following the defined
    reporting frequency.
    """
    
    measure = models.ForeignKey(
        Measure,
        on_delete=models.CASCADE,
        related_name="measure_reports",
        null=False,
        blank=False,
    )
    reported_value = models.CharField(max_length=20, null=False, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.PROTECT,
        related_name="created_measure_reports",
        null=False,
        blank=False,
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.PROTECT,
        related_name="updated_measure_reports",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.measure.reference_PDA.short_name} - {self.measure.id} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"


class ReportFile(models.Model):
    """
    Represents a file that acts as a verification method (or part of one) related 
    to the reporting of a measure's value.
    """
    
    report = models.ForeignKey(
        MeasureReport,
        on_delete=models.CASCADE,
        related_name="files",
        null=False,
        blank=False,
    )
    description = models.CharField(max_length=255, null=False, blank=False)
    file = models.FileField(upload_to="uploads/")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.PROTECT,
        related_name="created_report_files",
        null=False,
        blank=False,
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.PROTECT,
        related_name="updated_report_files",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.description}"


class Body(models.Model):
    """
    Represents a "sectorial body" involved with the environmental plans available
    in the system.
    """
    
    name = models.CharField(max_length=100, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.PROTECT,
        related_name="created_bodies",
        null=False,
        blank=False,
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.PROTECT,
        related_name="updated_bodies",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class BodyMeasure(models.Model):
    """
    Acts as the representation of the relationship between a Measure and a sectorial
    Body. A measure will always require at least one Body to be assigned to them, but
    multiple bodies can be involved, which makes this many-to-many linkage useful.
    """
    
    fk_measure = models.ForeignKey(
        Measure,
        on_delete=models.CASCADE,
        related_name="measure_bodymeasure",
        null=False,
        blank=False,
    )
    fk_body = models.ForeignKey(
        Body,
        on_delete=models.CASCADE,
        related_name="body_bodymeasure",
        null=False,
        blank=False,
    )
    is_reporter = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.PROTECT,
        related_name="created_bodymeasures",
        null=False,
        blank=False,
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.PROTECT,
        related_name="updated_bodymeasures",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.fk_body.name} - {self.fk_measure.short_name}"
