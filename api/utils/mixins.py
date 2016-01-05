from api import db
from flask_restful import abort


class BaseMixin(object):
    @classmethod
    def create(cls, commit=True, **kwargs):
        user = cls(**kwargs)
        db.session.add(user)
        if commit:
            db.session.commit()
        return user

    @classmethod
    def get_or_abort404(cls, id):
        rv = cls.query.get(id)
        if rv is None:
            abort(404)
        return rv

    @classmethod
    def get_by_or_abort404(cls, **kwargs):
        rv = cls.filter(**kwargs)
        if rv is None:
            abort(404)
        return rv[0]

    @classmethod
    def filter(cls, **kwargs):
        query = cls.query.filter_by(**kwargs)
        if kwargs.get('single', False):
            return query.first()
        return query.all()

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()

    def delete(self, commit=True):
        db.session.delete(self)
        if commit:
            db.session.commit()
