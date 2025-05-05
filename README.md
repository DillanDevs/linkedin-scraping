# LinkedIn Scraper & API Service

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.0+-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-blue.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Supported-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

Este proyecto automatiza la extracción de ofertas de trabajo de LinkedIn, las almacena en una base de datos PostgreSQL y expone un **API REST** para operaciones CRUD. Incluye además un script de automatización para backups y cargas incrementales.

---

## 📋 Objetivo

1. **Scraping** de LinkedIn con Selenium + BeautifulSoup (por renderizado JS)  
2. **Almacenamiento** en PostgreSQL (local o en la nube)  
3. **API REST** en FastAPI para crear, leer y eliminar ofertas  
4. **Automatización** de backups, limpieza de respaldos antiguos y cargas incrementales

---

## 🛠️ Pre-requisitos

- Python ≥ 3.13  
- Docker & Docker-Compose (opcional, para levantar PostgreSQL local)  
- ChromeDriver compatible con tu versión de Chrome  
- Credenciales de LinkedIn (usuario/contraseña)

---

## ⚙️ Configuración

### 1. Clonar y configurar el entorno

```bash
# Clonar el repositorio
git clone https://github.com/DillanDevs/linkedin_scraping.git
cd linkedin_scraping

# Crear variables de entorno
touch .env
```

### 2. Editar el archivo .env

```ini
LINKEDIN_USER=tu_usuario
LINKEDIN_PASS=tu_contraseña
DATABASE_URL=postgresql+psycopg2://backend:backend@localhost:5432/authdb
```

### 3. Levantar base de datos local con Docker-Compose

Asegúrate de tener este `docker-compose.yaml` en la raíz:

```yaml
version: "3.8"
services:
  db:
    image: postgres:14
    environment:
      POSTGRES_USER: backend
      POSTGRES_PASSWORD: backend
      POSTGRES_DB: authdb
    ports:
      - "5432:5432"
    volumes:
      - db_data:/var/lib/postgresql/data
volumes:
  db_data:
```

```bash
docker-compose up -d
```

### 4. Instalar dependencias

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## ▶️ Uso

### 1. Ejecutar Scraping

Extrae datos y los guarda en `dataset_linkedin.csv` y en la base de datos:

```bash
python -m scraping.pipeline
```

### 2. Arrancar API REST

```bash
uvicorn backend.main:app \
  --reload \
  --host 0.0.0.0 \
  --port 8000
```

Documentación interactiva disponible en: http://localhost:8000/docs

### 3. Automatización (opcional)

```bash
python -m backend.scripts.automation schedule
```

**Sub-comandos disponibles:**
- `scrape` → ejecuta scraping inmediato
- `backup` → realiza volcado completo con pg_dump
- `cleanup` → elimina respaldos más antiguos que RETENTION_DAYS

---

## 🏛️ Diagrama de arquitectura

![alt text](diagrama.png)

---

## 📂 Estructura del proyecto

```
linkedin_scraping/
├── .env                      # Variables de entorno
├── docker-compose.yaml       # Configuración de PostgreSQL local
├── requirements.txt          # Dependencias del proyecto
│
├── scraping/                 # Módulo de extracción de datos
│   ├── config.py             # Configuración del scraper
│   ├── driver.py             # Gestión de Selenium
│   ├── pipeline.py           # Pipeline completo de scraping
│   ├── scraper.py            # Lógica de scraping con BS4
│   ├── to_db.py              # Carga en base de datos
│   └── utils.py              # Utilidades
│
└── backend/                  # Servicio REST API
    ├── api/                  # Definición de rutas
    ├── config/               # Configuración
    ├── models/               # Modelos ORM
    ├── repository/           # Capa de acceso a datos
    ├── schemas/              # Esquemas Pydantic
    ├── services/             # Lógica de negocio
    ├── scripts/              # Scripts de automatización
    ├── utils/                # Utilidades y logging
    └── main.py               # Punto de entrada
```

---

## ✅ Recomendaciones

### Orden de ejecución:
1. Primero el pipeline de scraping (genera CSV + carga DB)
2. Luego el API para consultar los datos

### Entorno local vs nube:
- **Local**: Con Docker-Compose 
  ```
  DATABASE_URL=postgresql+psycopg2://backend:backend@localhost:5432/authdb
  ```
- **En nube**: Ajusta `DATABASE_URL` a tu RDS, Cloud SQL u otro servicio PostgreSQL

---

## 📊 Endpoints disponibles

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/jobs/` | Listar todas las ofertas de trabajo |
| GET | `/jobs/{id}` | Obtener oferta por ID |
| POST | `/jobs/` | Crear o actualizar múltiples ofertas |
| DELETE | `/jobs/{id}` | Eliminar oferta por ID |

---

## 📜 Licencia

Este proyecto está licenciado bajo la [Licencia MIT](LICENSE).

---

<div align="center">
Desarrollado por DillanDevs © 2025
</div>

