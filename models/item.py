from db import db


class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_name = db.Column(db.String(80), db.ForeignKey('stores.name'))
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_name):
        self.name = name
        self.price = price
        self.store_name = store_name

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'store_name': self.store_name
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_all(cls):
        return cls.query.all()