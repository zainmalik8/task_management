from fastapi import FastAPI

from .routers import user

app = FastAPI()

app_v1 = FastAPI()

app_v1.include_router(user.router_v1)


@app.get('/')
def root():
    return "Task management service."


app.mount("/api/v1", app_v1)
