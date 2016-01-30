from flask_restful import abort

from api import db


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
    def filter(cls, single=False, **kwargs):
        query = cls.query.filter_by(**kwargs)
        if single:
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

    def to_dict(self, exclude=None, include_private=False):
        dictionary = self.__dict__
        if exclude is None:
            exclude = []
        rv = {}
        for k, v in dictionary.iteritems():
            if include_private:
                rv[k] = v
            else:
                if k[0] != '_' and k not in exclude:
                    rv[k] = v

        return rv
