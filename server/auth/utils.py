from marshmallow import Schema, fields, validate


def isascii_not_empty(s):

    if not s:
        return False
    return len(s) == len(s.encode())


def valid_auth_string(s):

    if len(s) < 3 or len(s) > 16:
        return False
    return True


class UserSchema(Schema):
    username = fields.Str(required=True, validate=isascii_not_empty)
    password = fields.Str(required=True, validate=isascii_not_empty)
