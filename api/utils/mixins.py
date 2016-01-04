from api import db


class BaseMixin(object):
    @classmethod
    def create(cls, commit=True, **kwargs):
        user = cls(**kwargs)
        db.session.add(user)
        if commit:
            db.session.commit()
        return user

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()

    def delete(self, commit=True):
        db.session.delete(self)
        if commit:
            db.session.commit()
