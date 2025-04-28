# tf-sistema-reportes-ppda
Sistema de Reportes PPDA SEA - Grupo 2 - Desarrollo Backend Python - Talento Futuro

## Tecnologías principales

- Python 3.12.8
- Django Rest Framework
- PostgreSQL
- Swagger (documentación API)
- Pyenv (gestión de versiones de Python)

## Instalación del proyecto

### 1. Clonar el repositorio
```bash
git clone https://github.com/pmahuzieru/tf-sistema-reportes-ppda.git
cd tf-sistema-reportes-ppda
```

### 2. Configurar entorno Python (usando pyenv)
**macOS**
```bash
brew install openssl readline sqlite3 xz zlib
curl https://pyenv.run | bash
```

Luego, agregar `pyenv` a `.zshrc` (o `bashrc` en Linux o macOS antiguos, según corresponda)
```
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init --path)"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
source ~/.zshrc
````

**Windows**

Instalar Pyenv a través de `pyenv-win`.
```bash
curl -L https://github.com/pyenv-win/pyenv-win/releases/latest/download/pyenv-win.zip -o pyenv-win.zip
tar -xf pyenv-win.zip -C $HOME/.pyenv
```
Agregar los siguientes directorios a las variables de entorno del sistema.
```makefile
C:\Users\<Usuario>\.pyenv\pyenv-win\bin
C:\Users\<Usuario>\.pyenv\pyenv-win\shims
```

**Validar que pyenv quedó bien instalado**

Reiniciar terminal si es necesario
```bash
pyenv --version
```

**Instalar versión de python deseada**
```bash
pyenv install 3.12.8
pyenv local 3.12.8
```

### 3. Crear entorno virtual y activar
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv/Scripts/activate  # Windows
```

### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 5. Configurar archivo `.env``
Crear un archivo `.env.dev` y asegurarse de incluir al menos las siguientes variables del ejemplo:

```
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
SECRET_KEY=grupo-2-secret-key-dev
DATABASE_URL=postgres://<username>:<password>@localhost:5432/<database>
```

## Uso y desarrollo
### Ejecutar el servidor:
```bash
cd sistema_reportes_ppda
ENV_FILE=.env.dev python manage.py runserver
```
**Nota**: Es importante especificar `ENV_FILE=.env.dev` (o el archivo que corresponda) para contar con las variables de entorno adecuadas.

### Cargar datos de ejemplo
```bash
cd sistema_reportes_ppda

# Ejemplo
ENV_FILE=.env.dev python manage.py populate_data
```

### Swagger
1. Ingresar a localhost:8000/admin y crear un nuevo token para tu usuario.
2. Ingresar a localhost:8000/swagger
3. Seleccionar el boton superior derecho 'Authorize' y escribir: `Token <api_token>`
4. Testear los endpoints