from fastapi import HTTPException, status


class BadRequestException(HTTPException):
    def __init__(self, *args, status_code=None, detail=None, **kwargs, ):
        super().__init__(*args, **kwargs, status_code=status_code or status.HTTP_400_BAD_REQUEST,
                         detail=detail or "Something Went Wrong.")
