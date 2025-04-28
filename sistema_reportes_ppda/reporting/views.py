from rest_framework import viewsets
from reporting.models import ProgressReport
from reporting.serializers import ProgressReportSerializer
from custom_permissions import IsSMAUserOrAdmin
from drf_spectacular.utils import extend_schema


@extend_schema(
    tags=["Reportes de Avance"],
    summary="Gestión de informes de avance de un plan ambiental",
    description="""
Este endpoint permite consultar y administrar los **informes de avance anuales** (`ProgressReport`) de un `EnvironmentalPlan`.

Cada `ProgressReport` corresponde típicamente a un año calendario evaluado, según lo definido en el decreto del plan.

Al crear un nuevo `ProgressReport`, el sistema genera automáticamente los datos agregados (`ProgressReportData`) asociados al plan, útiles para análisis y visualización.

### Permisos:
- **Usuarios autenticados** pueden consultar (`list`, `retrieve`) los informes.
- **Solo usuarios de la SMA o administradores** pueden crear o modificar (`create`, `update`) reportes.

### Campos clave:
- `environmental_plan`: referencia al plan evaluado
- `publication_date`: fecha oficial del reporte
- `data_created`: indica si los datos fueron generados correctamente por el sistema
"""
)
class ProgressReportViewSet(viewsets.ModelViewSet):
    queryset = ProgressReport.objects.all()
    serializer_class = ProgressReportSerializer

    def get_permissions(self):
        """
        Only SMA/Admin can create/update progress reports.
        Default permissions applied to other actions.
        """
        if self.action in ["create", "update", "partial_update"]:
            return [IsSMAUserOrAdmin()]
        return super().get_permissions()

    def perform_create(self, serializer):
        # Automatically set the `created_by` field to the logged-in user
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        # Automatically set the `updated_by` field to the logged-in user
        serializer.save(updated_by=self.request.user)
