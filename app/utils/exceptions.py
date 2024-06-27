from fastapi import HTTPException, status


class BadRequestException(HTTPException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, status_code=status.HTTP_400_BAD_REQUEST, detail="Something Went Wrong.")
