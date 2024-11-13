import os
import subprocess
import platform

def run_command(command):
    process = subprocess.Popen(command, shell=True)
    process.communicate()

def create_virtualenv():
    print("\033[94m[INFO]\033[0m Creando entorno virtual...")
    run_command("python -m venv venv")
    print("\033[92m[OK]\033[0m Entorno virtual creado.")

def install_package(package, use_venv):
    pip_command = "venv\\Scripts\\pip" if platform.system() == "Windows" else "venv/bin/pip"
    if not use_venv:
        pip_command = "pip"
    run_command(f"{pip_command} install {package}")
    print(f"\033[92m[OK]\033[0m {package} instalado.")

def create_file(path, content):
    with open(path, "w") as f:
        f.write(content)
    print(f"\033[92m[OK]\033[0m {path} creado.")

def create_structure(project_options):
    os.makedirs("app", exist_ok=True)
    if project_options['include_templates']:
        os.makedirs("app/templates", exist_ok=True)
        create_file("app/templates/index.html", """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Flask App</title></head><body><h1>Hello, Flask!</h1></body></html>""")
    if project_options['include_static']:
        os.makedirs("app/static", exist_ok=True)
    if project_options['include_routes']:
        os.makedirs("app/routes", exist_ok=True)
        create_file("app/routes/main.py", """from flask import Blueprint, render_template\nbp = Blueprint('main', __name__)\n@bp.route('/')\ndef index():\n    return render_template('index.html')""")
    create_file("app/app.py", """from flask import Flask\napp = Flask(__name__)\nfrom app.routes import main\napp.register_blueprint(main.bp)\nif __name__ == "__main__":\n    app.run(debug=True)""")

def setup_database(db_choice):
    db_configs = {
        'sqlite': "SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'",
        'mysql': "SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@localhost/db_name'",
        'postgresql': "SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost/db_name'"
    }
    if db_choice in db_configs:
        create_file("config.py", db_configs[db_choice])

def add_authentication():
    os.makedirs("app/auth", exist_ok=True)
    create_file("app/auth/routes.py", """from flask import Blueprint, render_template, redirect, url_for\nauth_bp = Blueprint('auth', __name__)\n@auth_bp.route('/login')\ndef login():\n    return render_template('login.html')\n@auth_bp.route('/register')\ndef register():\n    return render_template('register.html')""")
    create_file("app/templates/login.html", "<h1>Login Page</h1>")
    create_file("app/templates/register.html", "<h1>Register Page</h1>")

def create_docker_files():
    create_file("Dockerfile", """# Dockerfile\nFROM python:3.9-slim\nWORKDIR /app\nCOPY . /app\nRUN pip install -r requirements.txt\nCMD ["python", "app/app.py"]""")
    create_file("docker-compose.yml", """version: '3.8'\nservices:\n  web:\n    build: .\n    ports:\n      - "5000:5000""")

def create_project_files(project_options):
    if project_options['env_file_choice']:
        create_file(".env", "SECRET_KEY=your_secret_key\nDATABASE_URL=your_database_url")
    if project_options['readme_choice']:
        create_file("README.md", f"# {project_options['project_name']}\n\nProyecto Flask configurado automáticamente.")
    license_texts = {
        'mit': "MIT License",
        'apache': "Apache License 2.0"
    }
    if project_options['license_choice'] in license_texts:
        create_file("LICENSE", license_texts[project_options['license_choice']])

def setup_flask_project():
    print("\033[96m[SETUP]\033[0m Configuración del proyecto Flask")
    project_options = {
        'project_name': input("Nombre del proyecto (Enter para 'FlaskProject'): ").strip() or "FlaskProject",
        'use_venv': input("¿Usar entorno virtual (s/n)? ").strip().lower() == 's',
        'install_flask_lib': input("¿Instalar Flask automáticamente (s/n)? ").strip().lower() == 's',
        'db_choice': input("¿Integrar base de datos (ninguna/sqlite/mysql/postgresql)? ").strip().lower(),
        'auth_choice': input("¿Agregar autenticación básica (s/n)? ").strip().lower() == 's',
        'env_config': input("¿Separar configuración dev/prod (s/n)? ").strip().lower() == 's',
        'extra_packages': input("Paquetes adicionales (separados por comas, vacío para ninguno): ").strip().split(",") if input("Paquetes adicionales (separados por comas, vacío para ninguno): ").strip() else [],
        'docker_choice': input("¿Crear Dockerfile y docker-compose.yml (s/n)? ").strip().lower() == 's',
        'frontend_choice': input("¿Integrar framework CSS (bootstrap/tailwind/ninguno)? ").strip().lower(),
        'env_file_choice': input("¿Crear archivo .env (s/n)? ").strip().lower() == 's',
        'readme_choice': input("¿Generar README.md? (s/n): ").strip().lower() == 's',
        'license_choice': input("¿Agregar licencia (MIT/Apache/ninguna): ").strip().lower()
    }
    
    os.makedirs(project_options['project_name'], exist_ok=True)
    os.chdir(project_options['project_name'])

    if project_options['use_venv']:
        create_virtualenv()
    if project_options['install_flask_lib']:
        install_package("Flask", project_options['use_venv'])
    create_structure({'include_templates': True, 'include_static': True, 'include_routes': True})
    if project_options['db_choice'] != "ninguna":
        setup_database(project_options['db_choice'])
    if project_options['auth_choice']:
        add_authentication()
    if project_options['extra_packages']:
        for package in project_options['extra_packages']:
            install_package(package.strip(), project_options['use_venv'])
    if project_options['docker_choice']:
        create_docker_files()
    if project_options['frontend_choice'] == "bootstrap":
        create_file("app/templates/base.html", """<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">""")
    elif project_options['frontend_choice'] == "tailwind":
        create_file("app/templates/base.html", """<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">""")
    create_project_files(project_options)
    
    print(f"\033[92m[FINALIZADO]\033[0m Proyecto Flask '{project_options['project_name']}' configurado exitosamente.")
    print("\n\033[93m¡Gracias por usar este script de configuración de Flask!\033[0m")
    print("\033[93mCreado por Luigi Adducci\033[0m")
    print("GitHub: \033[94mhttps://github.com/LuigiValentino\033[0m")

if __name__ == "__main__":
    setup_flask_project()
