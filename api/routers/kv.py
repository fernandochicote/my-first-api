from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from fastapi.responses import PlainTextResponse
from fastapi.security import HTTPBasicCredentials
from pydantic import BaseModel, Field
from db import redis
from logger import log
from security import *

router = APIRouter(tags=["kv"], prefix="/kv")

class HTTPExceptionModel(BaseModel):
    detail: str = Field(description="Error message", example="Client id not found")

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/token", summary="Login to get access token",
    responses={
        status.HTTP_200_OK: {"description": "Credentials validated. Token returned", "model": Token},
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid credentials", "model": HTTPExceptionModel},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal Error Server", "model": HTTPExceptionModel},
    }
)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    authenticate_user(form_data)
    access_token = create_access_token(data={"sub": form_data.username})
    return Token(access_token=access_token, token_type="bearer")

@router.get("/keys", summary="Get list of clients",
    responses={
        status.HTTP_200_OK: {"description": "Client list returned", "model": list[str]},
        status.HTTP_400_BAD_REQUEST: {"description": "Disabled user", "model": HTTPExceptionModel},
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid credentials", "model": HTTPExceptionModel},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal Error Server", "model": HTTPExceptionModel},
    }
)
async def get_client_list(current_user: UserSchema = Depends(get_validated_active_user)):
    log.info(f"Se devuelve la lista de clientes al usuario [{current_user.username}] con token válido y activo")
    return get_redis_keys()

def get_redis_keys():
    try:
        return redis.keys()
    except Exception as ex:
        log.error(f"Exception obteniendo lista claves de Redis error {ex}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@router.get("/{client_id}", 
            summary='Get client favourite movie',
            responses={
                status.HTTP_200_OK: {"description": "Movie returned"},
                status.HTTP_401_UNAUTHORIZED: {"description": "Not authenticated", "model": HTTPExceptionModel},
                status.HTTP_404_NOT_FOUND: {"description": "Client id not found", "model": HTTPExceptionModel},
                status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal Error Server", "model": HTTPExceptionModel}
                },
                response_class=PlainTextResponse)
def get_favourite_movie(client_id: str = Path(description="Client identifier", min_length=3), apikey: str = Depends(apikey_security)):
    validate_apikey(apikey)
    value = get_redis_value(client_id)
    msg = f"Client {client_id} not found"
    if not value:
        log.error(f"[GET] {msg}")
        raise HTTPException(detail=msg, status_code=status.HTTP_404_NOT_FOUND)
    return value

def get_redis_value(client_id: str):
    try:
        return redis.get(client_id)
    except Exception as ex:
        log.error(f"Exception obteniendo clave {client_id} de Redis error: {ex}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@router.post("/{client_id}", summary="Register client favourite movie",
    responses={
        status.HTTP_200_OK: {"description": "Favourite movie registered"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Not authenticated", "model": HTTPExceptionModel},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal Server Error", "model": HTTPExceptionModel},
    }
)
def register_favourite_movie(credentials: Annotated[HTTPBasicCredentials, Depends(basic_security)],
                             client_id: str = Path(description="Client identifier", min_length=3),
                             movie_title: str = Query(description="The favourite movie of the client", min_length=3),
                             expiration: int = Query(description="Expiration in ms", gt=0, example=10000, default=None)):
    validate_basic(credentials)
    result = set_redis(client_id, movie_title, expiration)
    msg = f"Error in Redis backend key {client_id} value {movie_title}"
    if result == False:
        log.error(f"[POST] {msg}")
        raise HTTPException(detail=msg, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return "OK"

def set_redis(key: str, value: str, expiration: int | None):
    try:
        if expiration:
            return redis.set(name=key, value=value, px=expiration)
        return redis.set(name=key, value=value)
    except Exception as ex:
        log.error(f"Exception almacenando clave {key} value {value} en Redis error: {ex}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")




