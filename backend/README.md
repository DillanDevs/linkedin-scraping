# Servicio Backend

Este backend ofrece una API REST para gestionar las ofertas de trabajo extraídas de LinkedIn. Está desarrollado en Python con **FastAPI**, siguiendo principios **SOLID** y arquitectura **hexagonal**.

---

## 🚀 Inicio rápido

1. **Clonar el repositorio**  
   ```bash
   git clone https://github.com/DillanDevs/linkedin-scraping.git
   cd linkedin_scraping
   ```

2. **Crear y activar entorno virtual**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r ../requirements.txt
   ```

4. **Configurar variables de entorno**  
   Copia en .env y ajusta:
   ```dotenv
   LINKEDIN_USER=<usuario>
   LINKEDIN_PASS=<clave>   
   DATABASE_URL=postgresql+psycopg2://<usuario>:<clave>@<host>:5432/<nombre_bd>
   ```

5. **Arrancar el servidor**
   ```bash
   uvicorn backend.main:app \
     --reload \
     --host 0.0.0.0 \
     --port 8000
   ```
   La API quedará disponible en http://localhost:8000

6. **Explorar documentación interactiva**  
   Abre en el navegador:
   ```
   http://localhost:8000/docs
   ```

## 🏗️ Estructura del proyecto

```
backend/
├── api/                      # Definición de rutas (routers.py)
├── config/                   # Configuración de base de datos (config_db.py)
├── db/                       # Base de modelos SQLAlchemy (base.py)
├── models/                   # Modelo ORM JobListing (job_listing.py)
├── repository/               # Acceso a datos y upsert (job_repository.py)
├── schemas/                  # Pydantic schemas y respuestas estandarizadas
│   ├── job_schema.py
│   └── response_schemas.py
├── services/                 # Lógica de negocio (job_service.py)
├── scripts/                  # CLI de automatización (automation.py)
├── utils/                    # Logger centralizado (logger.py)
└── main.py                   # App factory y arranque
```

## 🔐 Principios de diseño

### SOLID
- **Single Responsibility**: cada módulo tiene una única responsabilidad.
- **Open/Closed**: los repositorios y servicios admiten extensión sin modificar código existente.
- **Liskov Substitution**: los Pydantic models pueden sustituirse sin romper la lógica.
- **Interface Segregation**: los routers sólo dependen de las interfaces que necesitan.
- **Dependency Inversion**: la capa de servicios depende de abstractions (repositorios), no de implementaciones concretas.

### Arquitectura Hexagonal
- **Core**: JobService contiene la lógica de negocio.
- **Puertos**: Pydantic schemas definen los contratos de entrada/salida.
- **Adaptadores**: JobRepository se comunica con la base de datos via SQLAlchemy.

## ⚡ ¿Por qué FastAPI?

- **Alto rendimiento**: basado en ASGI, muy rápido.
- **Validación**: esquemas automáticos con Pydantic.
- **Documentación automática**: OpenAPI + Swagger en /docs sin configuración extra.
- **Ergonomía**: inyección de dependencias y soporte nativo a async.

## 📚 Endpoints

| Método | Ruta | Descripción | Cuerpo (request) | Respuesta (response) |
|--------|------|-------------|------------------|----------------------|
| POST | /jobs/ | Crear o actualizar múltiples ofertas | List[JobCreate] | ResponseModel |
| GET | /jobs/ | Listar todas las ofertas | — | ListResponseModel |
| GET | /jobs/{id} | Obtener una oferta por ID | — | SingleResponseModel |
| DELETE | /jobs/{id} | Eliminar una oferta por ID | — | ResponseModel |

En errores de validación o recurso no encontrado, se devuelve:
```json
{
  "status": "error",
  "message": "Job not found",
  "data": null
}
```

En éxito:
```json
{
  "status": "success",
  "message": "…",
  "data": { … }
}
```

## 🔧 Scripts y automatización

El CLI `backend/scripts/automation.py` permite:
- **scrape**: ejecutar pipeline de scraping ahora
- **backup**: volcar la base de datos a backups/
- **cleanup**: borrar respaldos antiguos (> RETENTION_DAYS)
- **schedule**: iniciar APScheduler con tareas cron diarias

```bash
python -m backend.scripts.automation schedule
```

## 📖 Más información

Documentación Swagger:
http://localhost:8000/docs
