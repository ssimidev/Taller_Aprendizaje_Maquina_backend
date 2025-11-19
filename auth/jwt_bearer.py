from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException
from .jwt_handler import decode_jwt

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        if credentials:
            token = credentials.credentials
            if decode_jwt(token) is None:
                raise HTTPException(status_code=403, detail="Token expirado o inválido")
            return token

        raise HTTPException(status_code=403, detail="Token faltante")
