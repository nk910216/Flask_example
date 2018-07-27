import base64

from marshmallow import Schema, fields


class PicturePostSchema(Schema):
    data = fields.Str(required=True)


def simple_check_isBase64(s):

    s_byte = s
    if isinstance(s, str):
        s_byte = str.encode(s)
        if len(s_byte) != len(s):
            return s_byte, False

    try:
        if base64.b64encode(base64.b64decode(s_byte)) == s_byte:
            return s_byte, True
    except Exception:
        pass
    return s_byte, False