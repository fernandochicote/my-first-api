from fastapi import APIRouter
from fastapi import Response, status
from  enum import Enum

router = APIRouter(tags=["holamundo"], prefix="/hola")

@router.get(path="/sencillo", summary = "Método GET que dice hola")
def hola():
    return {"msg": "Hola mundo!"}

@router.get(path="/todos", summary = "Método GET que dice hola a un id concreto")
def hola():
    return "OK"

class ColorEnum(str, Enum):
    rubio = 'rubio'
    moreno = 'moreno'
    pelirrojo = 'pelirrojo'

@router.get(path="/color/{color}", summary = "Método GET que dice hola a un color de pelo")
def hola(color: ColorEnum):
    return {"msg": f"Hola {color.name}!"}

@router.get(path="/edad", summary = "Método GET que dice hola según la edad")
def hola(edad: int, nombre: str = "Morty"):
    if edad < 42:
        return {"msg": f"Hola {nombre}"}
    else:
        return {"msg": f"Hola Sr. {nombre}"}
    
@router.get(path="/hola-si-hay-alguien", summary="Método GET que dice Hola si hay alguien", 
         response_description="Se responde porque hay alguien.", 
         responses={status.HTTP_200_OK: {"description": "Respuesta OK"},
                    status.HTTP_404_NOT_FOUND: {"description": "No hay nadie."}})
def hola(alguien: bool, response: Response):
    if alguien:
        return {"msg": "¡Hola hay alguien!"}
    else:
        response.status_code = 404
        return {"msg": "No hay nadie"}
    
