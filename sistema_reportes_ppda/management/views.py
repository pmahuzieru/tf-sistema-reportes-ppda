from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from management.models import (
    EnvironmentalPlan,
    Measure,
    MeasureReport,
    ReportFile,
    Body,
    BodyMeasure,
)
from management.serializers import (
    EnvironmentalPlanSerializer,
    MeasureReportSerializer,
    MeasureSerializer,
    ReportFileSerializer,
    BodySerializer,
    BodyMeasureSerializer,
)
from custom_permissions import IsAssignedToReportMeasure, IsSMAUserOrAdmin, ReportIsTheirs
from drf_spectacular.utils import extend_schema


@extend_schema(
    tags=["Planes Ambientales"],
    summary="Gestión de Planes de Descontaminación o Prevención (PPDA, PDA, PPA)",
    description="""
Este endpoint permite consultar y administrar los **planes ambientales** definidos por la SMA.

Un `EnvironmentalPlan` puede ser de tipo:
- `PPA`: Plan de Prevención Atmosférica
- `PDA`: Plan de Descontaminación Atmosférica
- `PPDA`: Plan de Prevención y Descontaminación Atmosférica

Cada plan puede contener múltiples `Measure` (medidas), y su progreso se evalúa a través de reportes.

### Permisos:
- **Usuarios autenticados** pueden consultar (`list` y `retrieve`) los planes.
- **Usuarios de la SMA o Admins** pueden crear, actualizar o eliminar planes.
"""
)
class EnvironmentalPlanViewSet(viewsets.ModelViewSet):
    queryset = EnvironmentalPlan.objects.all()
    serializer_class = EnvironmentalPlanSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]
        return [IsSMAUserOrAdmin()]

    def perform_create(self, serializer):
        # Automatically set the `created_by` field to the logged-in user
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        # Automatically set the `updated_by` field to the logged-in user
        serializer.save(updated_by=self.request.user)


@extend_schema(
    tags=["Medidas"],
    summary="Gestión de medidas de un plan ambiental",
    description="""
Este endpoint permite gestionar las **medidas** de un *Plan de Descontaminación o Prevención Atmosférica (PPDA/PDA/PPA)*.

### Permisos:
- **SMA/Admin**: pueden crear, actualizar y eliminar medidas.
- **Cualquier usuario autenticado**: puede ver (`list` y `retrieve`) las medidas disponibles.

### Campos relevantes:
- `measure_type`: tipo de medida (Regulación, Educación, Política Pública, etc.)
- `value_type`: tipo de valor reportado (boolean, integer, decimal, etc.)
- `reference_PDA`: referencia al plan ambiental correspondiente.
"""
)
class MeasureViewSet(viewsets.ModelViewSet):
    queryset = Measure.objects.all()
    serializer_class = MeasureSerializer

    def get_permissions(self):
        """
        Grant permissions based on action.
        """
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]  # I'm not sure if this is OK because the restriction above
        return [IsSMAUserOrAdmin()]  # Only SMA users can CRUD completely.

    def perform_create(self, serializer):
        # Automatically set the `created_by` field to the logged-in user
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        # Automatically set the `updated_by` field to the logged-in user
        serializer.save(updated_by=self.request.user)


@extend_schema(
    tags=["Reportes de Medidas"],
    summary="Registro de valores informados para medidas individuales",
    description="""
Este endpoint permite a los organismos responsables reportar valores específicos asociados al cumplimiento de una medida ambiental.

Cada `MeasureReport` representa **una declaración de un valor puntual** para una medida definida en un plan (`Measure`).

### Ejemplo:
- Medida: "N° de vehículos fiscalizados por mes"
- Valor informado (`reported_value`): "132"

El tipo de valor es validado automáticamente en función del `value_type` de la medida:
- booleano, entero, decimal, porcentaje, etc.

### Permisos:
- **Usuarios autenticados** pueden consultar (`list`, `retrieve`) los reportes.
- **Solo usuarios asignados a la medida** (vía `BodyMeasure`) pueden crear o modificar estos registros.
"""
)
class MeasureReportViewSet(viewsets.ModelViewSet):
    queryset = MeasureReport.objects.all()
    serializer_class = MeasureReportSerializer
    
    def get_permissions(self):
        """
        Grant permissions based on action.
        """
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]  # Anyone can read (for now)
        return [IsAssignedToReportMeasure()]  # Only users from assigned bodies

    def perform_create(self, serializer):
        # Automatically set the `created_by` field to the logged-in user
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        # Automatically set the `updated_by` field to the logged-in user
        serializer.save(updated_by=self.request.user)


@extend_schema(
    tags=["Archivos de Reportes"],
    summary="Gestión de archivos adjuntos a reportes de medidas",
    description="""
Este endpoint permite consultar, subir o modificar archivos adjuntos a un `MeasureReport`.

Los archivos pueden incluir:
- Evidencia del cumplimiento (planillas, informes, certificados, fotos)
- Documentos que respaldan el valor reportado

Cada `ReportFile` está vinculado a un único `MeasureReport`.

### Permisos:
- **Usuarios autenticados** pueden consultar (`list`, `retrieve`) los archivos.
- **Solo usuarios autorizados** (asignados al organismo del `MeasureReport`) pueden crear o modificar archivos.

### Restricciones:
- El archivo debe subirse usando `multipart/form-data`.
- El campo `report` (ID del reporte) debe estar especificado.
"""
)
class ReportFileViewSet(viewsets.ModelViewSet):
    queryset = ReportFile.objects.all()
    serializer_class = ReportFileSerializer
    
    def get_permissions(self):
        """
        Grant permissions based on action.
        """
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]  # Anyone can read (for now)
        return [ReportIsTheirs()]  # Only if the related reports is assigned to the user's body  

    def perform_create(self, serializer):
        # Automatically set the `created_by` field to the logged-in user
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        # Automatically set the `updated_by` field to the logged-in user
        serializer.save(updated_by=self.request.user)


@extend_schema(
    tags=["Organismos Responsables"],
    summary="Consulta y gestión de organismos responsables de medidas",
    description="""
Este endpoint permite consultar y administrar los **organismos (Body)** responsables de implementar o reportar medidas dentro de un plan ambiental.

Cada `Body` representa una entidad como:
- Un servicio público (ej. SEREMI, DGA, CONAF)
- Un municipio
- Una empresa u otra organización involucrada en el cumplimiento de medidas

Estas entidades pueden ser vinculadas a medidas a través del modelo `BodyMeasure`.

### Permisos:
- **Usuarios autenticados** pueden consultar (`list`, `retrieve`) los organismos.
- **Solo administradores** pueden crear, modificar o eliminar organismos, ya que se consideran entidades fijas dentro del sistema.
"""
)
class BodyViewSet(viewsets.ModelViewSet):
    queryset = Body.objects.all()
    serializer_class = BodySerializer
    
    def get_permissions(self):
        """
        Grant permissions based on action.
        """
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]  
        return [IsAdminUser()]  # Because of fixed nature of the objects, only allow Admins to modify list

    def perform_create(self, serializer):
        # Automatically set the `created_by` field to the logged-in user
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        # Automatically set the `updated_by` field to the logged-in user
        serializer.save(updated_by=self.request.user)


@extend_schema(
    tags=["Asignación de Responsabilidad"],
    summary="Asignación de medidas a organismos responsables",
    description="""
Este endpoint administra la asignación de **medidas** (`Measure`) a **organismos** (`Body`) dentro de un plan ambiental.

Cada `BodyMeasure` representa una relación que indica:
- Qué organismo está vinculado a una medida
- Si el organismo debe reportar avances (`is_reporter`)
- Si la asignación está activa o no (`active`)

Esta asignación permite controlar:
- Qué usuarios pueden declarar valores (`MeasureReport`)
- Qué organismos aparecen como responsables en reportes

### Permisos:
- **Usuarios autenticados** pueden consultar (`list`, `retrieve`) las asignaciones.
- **Solo usuarios SMA o administradores** pueden crear o modificar estas relaciones.
"""
)
class BodyMeasureViewSet(viewsets.ModelViewSet):
    queryset = BodyMeasure.objects.all()
    serializer_class = BodyMeasureSerializer

    def get_permissions(self):
        """
        Grant permissions based on action.
        """
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]  
        return [IsSMAUserOrAdmin()]  # Only allow SMA users to write these
    
    def perform_create(self, serializer):
        # Automatically set the `created_by` field to the logged-in user
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        # Automatically set the `updated_by` field to the logged-in user
        serializer.save(updated_by=self.request.user)
