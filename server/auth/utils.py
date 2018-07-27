from marshmallow import Schema, fields, validate


def isascii_not_empty(s):

    if not s:
        return False
    return len(s) == len(s.encode())


class UserSchema(Schema):
    username = fields.Str(required=True, validate=isascii_not_empty)
    password = fields.Str(required=True, validate=isascii_not_empty)
