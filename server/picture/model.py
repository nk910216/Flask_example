import uuid

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from server.extensions import db, STRING_LEN


Column = db.Column


class Picture(db.Model):
    """ Picture database
    """
    __table__name = 'picture'

    id = Column('Id', db.Integer, primary_key=True, autoincrement=True)
    data = Column('data', db.Binary, nullable=False)

    author_id = Column('AuthorID', db.String(STRING_LEN),
                       db.ForeignKey('user.Id',
                       ondelete='SET NULL',
                       onupdate='CASCADE'))

    author = db.relationship("User",
                             backref=db.backref("pictures", lazy='dynamic'),
                             lazy=True)

    def __init__(self):
        pass

    def set_data(self, data, author_id):
        self.data = data
        self.author_id = author_id

    def add_picture(self):
        try:
            Picture.query.filter_by(id=self.id).one()
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
                raise e


