class InvalidPostContent(Exception):
    pass


class UserAlreadyExist(Exception):
    pass


class UsernameNotExist(Exception):
    pass


class UserWrongPassword(Exception):
    pass


class JWTExpireTime(Exception):
    pass


class InvalidJWTToken(Exception):
    pass
