# Scraping Module

Este módulo se encarga de extraer (scrapear) ofertas de trabajo de LinkedIn y volcarlas en un CSV y en la base de datos.

---

## 📦 Estructura

```
scraping/
├── config.py # Ajustes y credenciales (pydantic Settings)
├── driver.py # Inicialización y login de Selenium
├── scraper.py # Lógica de extracción con BeautifulSoup
├── to_db.py # Carga del CSV en la base de datos via repositorio
└── utils.py # Funciones auxiliares (conteo de aplicantes, normalización de URL)
```

## 🔧 Uso

### Ejecutar pipeline completo

```bash
python -m scraping.pipeline
```

Esto:
- Arranca Selenium (headless Chrome)
- Hace login en LinkedIn
- Desplaza la página para cargar hasta JOB_LIMIT resultados
- Extrae campos y guarda dataset_linkedin.csv
- Volca el CSV a la base de datos configurada

## 📑 Campos extraídos

| Campo | Descripción |
|-------|-------------|
| title | Título de la oferta. Ej: "Python Developer" |
| company | Nombre de la empresa. Ej: "Capgemini" |
| location | Ubicación geográfica. Ej: "Nueva York, Estados Unidos" |
| date_posted | Fecha ISO de publicación. Ej: 2025-04-30 |
| days_since_posted | Días transcurridos desde date_posted hasta hoy |
| job_url | URL canónica de la oferta (sin parámetros de tracking) |
| applicants | Número de aplicantes reportados en la página de la oferta |

## 🛠 Elección de tecnologías

**Selenium + headless Chrome**:
- LinkedIn carga los listados y el botón "Ver más" mediante JavaScript, por lo que requests + BeautifulSoup no obtendría el HTML completo.

**BeautifulSoup**:
- Una vez renderizada la página por Selenium, se parsea el DOM estático con BS4 para extraer selectores CSS de forma sencilla y robusta.

**Pandas**:
- Para normalizar y volcar los datos a CSV.

**SQLAlchemy + repositorio (to_db.py)**:
- Para hacer un upsert eficiente en la base de datos relacional.

## 🔒 Consideraciones

**Respeto a robots.txt y términos de uso**:
- No está permitida la descarga masiva de información. Este scraper introduce retrasos (SCRAPE_DELAY) entre acciones para simular un uso humano.

**Configuración por entorno**:
- Todos los parámetros (credenciales, timeouts, límites) son variables de entorno gestionadas con Pydantic Settings.