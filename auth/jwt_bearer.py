from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException
from .jwt_handler import decode_jwt

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        if not credentials:
            raise HTTPException(status_code=403, detail="Token faltante")

        token = credentials.credentials
        payload = decode_jwt(token)

        if payload is None:
            raise HTTPException(status_code=403, detail="Token expirado o inválido")

        return payload["user_id"]  
