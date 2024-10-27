from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
from  routers import holamundo, movies, kv
from logger import log

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

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)

