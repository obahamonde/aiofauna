from typing import Generic, Literal, TypeVar

from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module

StatusCode = Literal[
    100,
    101,
    102,
    103,
    200,
    201,
    202,
    203,
    204,
    205,
    206,
    207,
    208,
    226,
    300,
    301,
    302,
    303,
    304,
    305,
    307,
    308,
    400,
    401,
    402,
    403,
    404,
    405,
    406,
    407,
    408,
    409,
    410,
    411,
    412,
    413,
    414,
    415,
    416,
    417,
    418,
    421,
    422,
    423,
    424,
    425,
    426,
    428,
    429,
    431,
    451,
    500,
    501,
    502,
    503,
    504,
    505,
    506,
    507,
    508,
    510,
    511,
]


Status = Literal["success", "error", "warning", "info"]

E = TypeVar("E", bound=Exception)


class AioFaunaException(Generic[E]):
    """Exception with status code, message, and status."""

    status_code: StatusCode
    message: str = Field(
        default="[The description from MDN]", description="The description from MDN"
    )
    status: Status = Field(default="error", description="The status of the exception")
    origin: str = Field(default="aiofauna", description="The origin of the exception")

    def json(self):
        return {"status": self.status, "message": self.message}

    def __repr__(self):
        return f"{self.__doc__}: {self.status_code} {self.message}"


class HttpException(AioFaunaException[Exception]):
    """Exception: An HTTP exception with status code, message, and status."""

    status_code: StatusCode
    message: str = Field(
        default="[The description from MDN]", description="The description from MDN"
    )
    status: Status = Field(default="error", description="The status of the exception")
    origin: str = Field(
        default="http server", description="The origin of the exception"
    )


class BadRequest(HttpException):
    """Exception: 400 Bad Request exception."""

    status_code: StatusCode = 400
    message: str = Field(default="Bad Request", description="Bad Request")
    status: Status = Field(default="error", description="The status of the exception")


class Unauthorized(HttpException):
    """Exception: 401 Unauthorized exception."""

    status_code: StatusCode = 401
    message: str = Field(default="Unauthorized", description="Unauthorized")
    status: Status = Field(default="error", description="The status of the exception")


class NotFound(HttpException):
    """Exception: 404 Not Found exception."""

    status_code: StatusCode = 404
    message: str = Field(default="Not Found", description="Not Found")
    status: Status = Field(default="error", description="The status of the exception")


class MethodNotAllowed(HttpException):
    """Exception: 405 Method Not Allowed exception."""

    status_code: StatusCode = 405
    message: str = Field(default="Method Not Allowed", description="Method Not Allowed")
    status: Status = Field(default="error", description="The status of the exception")


class InternalServerError(HttpException):
    """Exception: 500 Internal Server Error exception."""

    status_code: StatusCode = 500
    message: str = Field(
        default="Internal Server Error", description="Internal Server Error"
    )
    status: Status = Field(default="error", description="The status of the exception")


class NotImplemented_(HttpException):
    """Exception: 501 Not Implemented exception."""

    status_code: StatusCode = 501
    message: str = Field(default="Not Implemented", description="Not Implemented")
    status: Status = Field(default="error", description="The status of the exception")


class ServiceUnavailable(HttpException):
    """Exception: 503 Service Unavailable exception."""

    status_code: StatusCode = 503
    message: str = Field(
        default="Service Unavailable", description="Service Unavailable"
    )
    status: Status = Field(default="error", description="The status of the exception")


class GatewayTimeout(HttpException):
    """Exception: 504 Gateway Timeout exception."""

    status_code: StatusCode = 504
    message: str = Field(default="Gateway Timeout", description="Gateway Timeout")
    status: Status = Field(default="error", description="The status of the exception")


class TooManyRequests(HttpException):
    """Exception: 429 Too Many Requests exception."""

    status_code: StatusCode = 429
    message: str = Field(default="Too Many Requests", description="Too Many Requests")
    status: Status = Field(default="error", description="The status of the exception")


class Forbidden(HttpException):
    """Exception: 403 Forbidden exception."""

    status_code: StatusCode = 403
    message: str = Field(default="Forbidden", description="Forbidden")
    status: Status = Field(default="error", description="The status of the exception")


class Conflict(HttpException):
    """Exception: 409 Conflict exception."""

    status_code: StatusCode = 409
    message: str = Field(default="Conflict", description="Conflict")
    status: Status = Field(default="error", description="The status of the exception")


class UnprocessableEntity(HttpException):
    """Exception: 422 Unprocessable Entity exception."""

    status_code: StatusCode = 422
    message: str = Field(
        default="Unprocessable Entity", description="Unprocessable Entity"
    )
    status: Status = Field(default="error", description="The status of the exception")