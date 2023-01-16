from sqlalchemy import Integer, ForeignKey

from backend import db


class Dataset(db.Model):
    __tablename__ = "dataset"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    is_public = db.Column(db.Integer, nullable=True)
    data_schema = db.Column(db.String(254))
    user_id = db.Column(Integer, ForeignKey('user.id'))

    def to_dict(self):
        return {
            "data_schema": self.data_schema,
            "name": self.name,
            "id": self.id,
        }
