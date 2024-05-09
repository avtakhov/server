import datetime

import fastapi
from sqladmin.authentication import AuthenticationBackend
from jose import jwt

from .settings import settings


def check_authorization(api_key: str = fastapi.Header(None)):
    if api_key != settings.api_key:
        raise fastapi.HTTPException(status_code=401, detail="Unauthorized")

    return api_key


def create_jwt_token(data: dict, expiration_delta: datetime.timedelta) -> str:
    expiration = datetime.datetime.utcnow() + expiration_delta
    data.update({"exp": expiration})
    return jwt.encode(data, settings.secret_key, algorithm=settings.algorithm)


def create_access_token() -> str:
    return create_jwt_token(
        {"scopes": "access_token"},
        datetime.timedelta(minutes=30),
    )


def check_admin_token(token) -> bool:
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        return payload is not None
    except (jwt.ExpiredSignatureError, jwt.JWTError):
        return False


class AdminAuth(AuthenticationBackend):
    async def login(self, request: fastapi.Request) -> bool:
        form = await request.form()
        password = form["password"]

        if password != settings.sqladmin_password:
            return False

        # And update session
        token = create_access_token()
        request.session.update({"token": token})

        return True

    async def logout(self, request: fastapi.Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: fastapi.Request) -> bool:
        token = request.session.get("token")

        if not token or not check_admin_token(token):
            return False

        return True
