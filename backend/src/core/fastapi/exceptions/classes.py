from fastapi import HTTPException, status


class BadRequestException(HTTPException):
    def __init__(self):
        """Construct bad request error instance."""
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST)


class UnauthorizedException(HTTPException):
    def __init__(self):
        """Construct unathorized request error instance."""
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED)


class UnsupportedMediaTypeException(HTTPException):
    def __init__(self):
        """Construct unsupported media error instance."""
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED)


class ForbiddenException(HTTPException):
    def __init__(self):
        """Construct forbidden operation instance."""
        super().__init__(status_code=status.HTTP_403_FORBIDDEN)


class NotFoundException(HTTPException):
    def __init__(self, message: str):
        """Construct not found artifact error instance."""
        super().__init__(status_code=status.HTTP_404_NOT_FOUND)
        self.detail = message


class ConflictException(HTTPException):
    def __init__(self):
        """Construct conflict error instance."""
        super().__init__(status_code=status.HTTP_409_CONFLICT)


class InternalServerException(HTTPException):
    def __init__(self, detail):
        """Construct internal server error instance."""
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.detail = detail

    def __str__(self):
        return self.detail
