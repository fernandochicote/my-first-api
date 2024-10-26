
# My First API

Este es un proyecto de ejemplo para mostrar las funcionalidades básicas de una API construida con [FastAPI](https://fastapi.tiangolo.com/). La aplicación incluye endpoints de ejemplo para manejar películas y una funcionalidad básica de "hola mundo".

## Características

- CRUD para gestionar una colección de películas.
- Documentación automática de la API con OpenAPI.
- Configuración de Docker y Docker Compose para el despliegue.

## Estructura del Proyecto

```
MY-FIRST-API/
├── api/
│   ├── routers/
│   │   ├── holamundo.py          # Endpoint de ejemplo para "hola mundo"
│   │   ├── movies.py             # Endpoints CRUD para películas
│   ├── test/
│   │   ├── test_holamundo.py     # Pruebas unitarias para el endpoint "hola mundo"
│   ├── Dockerfile                # Archivo Docker para construir la imagen
│   ├── logger.py                 # Configuración del logger
│   ├── main.py                   # Punto de entrada principal de la aplicación
├── docker-compose.yml            # Configuración de Docker Compose
├── requirements.txt              # Dependencias del proyecto
├── .gitignore                    # Archivos y carpetas ignoradas por Git
├── LICENSE                       # Licencia del proyecto
└── README.md                     # Descripción general del proyecto
```

## Requisitos

- Python 3.12 o superior
- Docker (opcional, para despliegue en contenedor)

## Instalación

1. Clona este repositorio:

   ```bash
   git clone https://github.com/tu-usuario/my-first-api.git
   cd my-first-api
   ```

2. Crea un entorno virtual y activa el entorno:

   ```bash
   python -m venv env
   source env/bin/activate   # En macOS/Linux
   .\env\Scripts\activate    # En Windows
   ```

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

## Uso

Para ejecutar la aplicación localmente:

```bash
uvicorn api.main:app --reload
```

La API estará disponible en `http://127.0.0.1:8000`.

## Endpoints Principales

### `GET /movies/{id}`

Obtiene una película por su ID.

### `POST /movies`

Crea una nueva película.

### `PUT /movies/{id}`

Actualiza una película existente.

### `DELETE /movies/{id}`

Elimina una película.

### `GET /`

Redirige automáticamente a la documentación de la API.

## Docker Compose

Este proyecto incluye un archivo `docker-compose.yml` para facilitar el despliegue en un entorno Dockerizado.

1. Construye y ejecuta la aplicación usando Docker Compose:

   ```bash
   docker-compose up --build
   ```

2. La API estará disponible en `http://localhost:8000`.

Para detener y remover los contenedores:

```bash
docker-compose down
```

## Pruebas

Para ejecutar las pruebas:

```bash
pytest
```

## Licencia

Este proyecto está licenciado bajo la **GNU General Public License**. Consulta el archivo [LICENSE](LICENSE) para más detalles.