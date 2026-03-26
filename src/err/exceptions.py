from fastapi import HTTPException, status


class AppException(HTTPException):
    def __init__(self, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                 detail="An error occured while processing request."):
        self.detail = detail
        self.status_code = status_code

class NotFoundException(AppException):
    def __init__(self, detail="Resource not found"):
        super().__init__(detail=detail, status_code=status.HTTP_404_NOT_FOUND)
        