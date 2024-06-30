from fastapi import FastAPI, Depends

from .auth_dependency import JWTBearer
from .dependencies import get_db
from .routers import user, profile, project, user_managment, task, comment
from .settings import JwtCreds

app = FastAPI()

app_v1 = FastAPI(dependencies=[Depends(get_db)])

app_v1.include_router(user.router_v1)

for router in [profile.router_v1, project.router_v1, user_managment.router_v1, task.router_v1, comment.router_v1]:
    app_v1.include_router(router, dependencies=[Depends(JWTBearer(**JwtCreds.get_creds()))])


@app.get('/')
def root():
    return "Task management service."


app.mount("/v1", app_v1)
