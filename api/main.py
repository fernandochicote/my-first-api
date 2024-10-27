from fastapi import FastAPI, HTTPException, Request
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import RedirectResponse
import uvicorn
from  routers import holamundo, movies, kv
from logger import log
from elasticapm.contrib.starlette import ElasticAPM, make_apm_client

descripcion = 'Aplicación sencilla para mostrar funcionalidades de FastAPI'

app = FastAPI(description=descripcion,
            version='0.0.3',
            title='Máster EOI - FastAPI API',
            contact={ "name": "Fernando Chicote",
                        "url": "https://github.com/fernandochicote",
                        "email": "fechicot@gmail.com"},
            license_info={
                        "name": "GPL-3.0",
                        "url": "https://www.gnu.org/licenses/gpl-3.0.html",
                    },
            openapi_tags = [
                                {
                                    "name": "holamundo",
                                    "description": "Operations para saludar",
                                },
                                                                {
                                    "name": "movies",
                                    "description": "Operations CRUD sobre peliculas",
                                },
                                                                {
                                    "name": "kv",
                                    "description": "Operaciones clave-valor",
                                }
                        ]                   
)

# API Routers
app.include_router(holamundo.router)
app.include_router(movies.router)
app.include_router(kv.router)

@app.get("/", include_in_schema=False)
def redirigir():
    log.info("Petición a /, redirigiendo a /docs.")
    return RedirectResponse(url="/docs")

# APM

# APM
apm = make_apm_client({
    'SERVICE_NAME': 'fastapi-api',
    'DEBUG': True,
    'SERVER_URL': 'http://apm-server:8200',
    'CAPTURE_HEADERS': True,
    'CAPTURE_BODY': 'all'
})

app.add_middleware(ElasticAPM, client=apm)

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    log.info(f"Capturando HTTPException motivo {exc.detail}")
    apm.capture_exception()
    return await http_exception_handler(request, exc)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)

