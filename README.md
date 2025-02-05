# tf-sistema-reportes-ppda
Sistema de Reportes PPDA SEA - Grupo 2 - Desarrollo Backend Python - Talento Futuro


# Swagger
1. Ingresar a localhost:8000/admin y crear un nuevo token para tu usuario.
2. Ingresar a localhost:8000/swagger
3. Seleccionar el boton superior derecho 'Authorize' y escribir: `Token <api_token>`
4. Testear los endpoints


# Llenar la base de datos
1. Desde la carpeta del proyecto ejecutar los siguientes comandos:
python manage.py loaddata fixtures/environmental_plans.json
python manage.py loaddata fixtures/measures.json
