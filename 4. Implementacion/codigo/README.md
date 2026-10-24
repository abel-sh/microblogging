# MiBlog

Sistema de microblogging para empleados de una empresa. Trabajo de Ingeniería de Software.

Tecnología: Python 3.10 o más nuevo, Flask, plantillas Jinja2, SQLite (`sqlite3`), python-dotenv.

## Cómo arrancarlo

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env          # y editá SECRET_KEY

flask --app miblog iniciar-bd # crea instance/miblog.sqlite3 (una sola vez)
flask --app miblog run        # abre http://127.0.0.1:5000
```

## Estructura

Ver `DISEÑO_MiBlog.md`, sección 2.4.