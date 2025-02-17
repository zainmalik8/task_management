from jose import jwt

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.logger import logger


class JWTBearer(HTTPBearer):
    """
    JWTBearer is a wrapper class of FastAPI HTTPBearer, this class with authorize the authentic requests.
    and get the user_Id from decoded token.
    """

    def __init__(self, secret_key: str, algorithm: str, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.secret_key, self.algorithm = secret_key, algorithm

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if credentials.scheme != "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if user := self.verify_jwt(credentials.credentials):
                request.state.user_id, request.state.user_role = user.get('user_id'), user.get("user_role")
                if not self.permission_handler(request):
                    raise HTTPException(status_code=403, detail="Request Forbidden.")
                return credentials.credentials
            raise HTTPException(status_code=403, detail="Invalid token or expired token.")
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, credentials: str) -> dict:
        """
        This will verify the token and return user_id, if jwt has valid signature.

        :param credentials: token used to verify the jwt
        :return:
        """
        try:
            decoded_jwt = jwt.decode(credentials, self.secret_key, algorithms=[self.algorithm])
            decoded_jwt.pop("exp")
            return decoded_jwt
        except Exception as error:
            logger.error(error)

    @staticmethod
    def permission_handler(request: Request) -> bool:
        """

        :param request: An instance of starlette request object
        :return: boolean based on the roles and methods
        """
        scope, user_id, user_role = request.scope, request.state.user_id, request.state.user_role
        api, method = scope.get('path').strip('/'), scope.get('method').lower()
        if "admin" in api:
            if user_role.lower() == "admin":
                return True
        else:
            return True
