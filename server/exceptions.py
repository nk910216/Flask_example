class InvalidPostContent(Exception):
    pass


class UserAlreadyExist(Exception):
    pass


class UsernameNotExist(Exception):
    pass


class UserWrongPassword(Exception):
    pass


class InvalidPictureFormat(Exception):
    pass


class JWTExpireTime(Exception):
    pass


class InvalidJWTToken(Exception):
    pass


class NoAuthToken(Exception):
    pass


class UploadPictureFail(Exception):
    pass


class InvalidArgs(Exception):
    pass