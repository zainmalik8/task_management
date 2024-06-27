from fastapi import FastAPI, Depends

from .auth_dependency import JWTBearer
from .dependencies import get_db
from .routers import user, profile
from .settings import JwtCreds

app = FastAPI()

app_v1 = FastAPI(dependencies=[Depends(get_db)])

app_v1.include_router(user.router_v1)
app_v1.include_router(profile.router_v1, dependencies=[Depends(JWTBearer(**JwtCreds.get_creds()))])


@app.get('/')
def root():
    return "Task management service."


app.mount("/api/v1", app_v1)
