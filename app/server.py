import uvicorn

from app.main import app  # noqa
from app.settings import BaseEnv

if __name__ == '__main__':
    host, port = BaseEnv().service_domain.split(':')
    uvicorn.run("app.main:app", host=host, port=int(port), reload=True)
