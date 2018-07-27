import binascii
import hashlib
import secrets
import uuid

from flask import current_app
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from server.extensions import db, STRING_LEN

Column = db.Column


class User(db.Model):
    """ User database.
    """

    __tablename__ = 'user'

    id = Column('Id', db.String(STRING_LEN), primary_key=True)
    username = Column('Username', db.String(STRING_LEN), unique=True, nullable=False)
    password_sault = Column('PasswordSault', db.Binary(STRING_LEN), nullable=False)
    password_hash = Column('PasswordHash', db.Binary(STRING_LEN), nullable=False)

    def __init__(self):
        self.id = uuid.uuid4().hex

    def __str__(self):
        return "{}(ID: {})".format(self.username, self.id)

    @classmethod
    def hash_password(cls, salt, password):
        dk = hashlib.pbkdf2_hmac('sha256', bytes(password, 'utf8'), salt, 10000)
        pwhash = binascii.hexlify(dk)
        return pwhash

    def set_data(self, username, password):
        salt = bytes(secrets.token_hex(16), 'utf8')

        pwhash = self.hash_password(salt, password)

        self.username = username
        self.password_sault = salt
        self.password_hash = bytes(pwhash)

    def verify_user(self, password):
        pwhash = self.hash_password(self.password_sault, password)

        return self.password_hash == pwhash

    def add_user(self):
        try:
            User.query.filter_by(username=self.username).one()
            return False
        except NoResultFound:
            try:
                db.session.add(self)
                db.session.commit()
                return True
            except IntegrityError:
                db.session.rollback()
                return False
            except Exception as e:
                db.session.rollback()
                current_app.logger.error(e)
                raise e


