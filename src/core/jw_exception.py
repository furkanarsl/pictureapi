import jwt
from fastapi import Request
from starlette import status
from starlette.responses import JSONResponse


async def jwt_exception_handler(request: Request, exc: jwt.PyJWTError):
    status_code = 403
    detail = "Could not validate credentials"

    if type(exc) == jwt.InvalidTokenError:
        status_code = 422
    elif type(exc) == jwt.InvalidIssuerError:
        status_code = 422
    elif type(exc) == jwt.InvalidAudienceError:
        status_code = 422
    elif type(exc) == jwt.InvalidIssuedAtError:
        status_code = 422
    elif type(exc) == jwt.ExpiredSignatureError:
        status_code = 403
    elif type(exc) == jwt.InvalidAlgorithmError:
        status_code = 422
    elif type(exc) == jwt.InvalidSignatureError:
        status_code = 422
    elif type(exc) == jwt.ImmatureSignatureError:
        status_code = 403
    elif type(exc) == jwt.MissingRequiredClaimError:
        status_code = 403
    elif type(exc) == jwt.DecodeError:
        status_code = 422

    detail = exc.args[0]
    return JSONResponse(status_code=status_code,
                        content={"detail": detail})
