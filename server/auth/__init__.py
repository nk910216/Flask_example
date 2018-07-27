from functools import wraps

from flask import request
import jwt
from sqlalchemy.orm.exc import NoResultFound

from server.exceptions import (NoAuthToken,
                               JWTExpireTime,
                               InvalidJWTToken,
                               UsernameNotExist)

from .view import RegisterHandler, LoginHandler
from .model import User


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_token = request.headers.get('Authorization')
        if not auth_token:
            raise NoAuthToken

        try:
            user_id = User.decode_auth_token(auth_token)
        except jwt.ExpiredSignatureError:
            raise JWTExpireTime
        except jwt.InvalidTokenError:
            raise InvalidJWTToken

        try:
            user = User.query.filter_by(id=user_id).one()
        except NoResultFound:
            raise UsernameNotExist

        # real function
        return f(user=user, *args, **kwargs)

    return decorated_function
