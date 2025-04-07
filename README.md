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


# Instrucciones para configurar el proyecto en su computador

## 1. Clonar el reporte

En una carpeta de su computador donde quieran dejar el repo (teniendo git instalado) 
escriben

```
git clone https://github.com/pmahuzieru/tf-sistema-reportes-ppda.git
```

## 2. Instalar pyenv para gestionar la versión de Python del proyecto

### En macOS (con homebrew)

1. Install pyenv dependencies: For Linux (Ubuntu/Debian-based systems) and macOS, you need to install some dependencies first. Run the following commands:

```
brew install openssl readline sqlite3 xz zlib
```
2. Install pyenv: Install pyenv using curl:
```
curl https://pyenv.run | bash
```
3. Update your shell configuration: After installing, add pyenv to your shell startup file. This ensures that pyenv is available every time you open a terminal.

    For Bash (common on Linux and older macOS):
```
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
source ~/.bashrc
```
For Zsh (common on newer macOS):

```
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init --path)"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
source ~/.zshrc
```

4. Verify the installation: After running the above commands, verify that pyenv is installed:
```
pyenv --version
```

### En Windows

1. Install pyenv on Windows: On Windows, pyenv is available through a tool called pyenv-win. Install pyenv-win by running:

```
curl -L https://github.com/pyenv-win/pyenv-win/releases/latest/download/pyenv-win.zip -o pyenv-win.zip
tar -xf pyenv-win.zip -C $HOME/.pyenv
```

2. Add pyenv to system path: Add the following to your environment variables:

```
C:\Users\<Your-Username>\.pyenv\pyenv-win\bin
C:\Users\<Your-Username>\.pyenv\pyenv-win\shims
```

3. Verify installation: Run:
```
pyenv --version
```

# 3. Instalar python 3.12.8 para el proyecto

Once pyenv is installed, you can use it to install Python 3.12.8:
```
pyenv install 3.12.8
```

Set Python 3.12.8 as the local version for your project: In the root directory of your project (inside tf-sisstema-reportes-ppda), run:
```
pyenv local 3.12.8
```
This will create a .python-version file in your project directory with the Python version you selected. This ensures that anyone who clones the repository and uses pyenv will automatically switch to Python 3.12.8.

Verify the Python version: After setting it, you can check the version:
```
python --version
```
It should return Python 3.12.8.