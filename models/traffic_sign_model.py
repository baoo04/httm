from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class TrafficSignModel(db.Model):
    __tablename__ = "tblTrafficSignModel"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    version = db.Column(db.Integer)
    pre = db.Column(db.Float)
    recall = db.Column(db.Float)
    f1_score = db.Column(db.Float)
    is_active = db.Column(db.Boolean, default=False)
    sample_quantity = db.Column(db.Integer)
    dataset_id = db.Column(db.Integer, db.ForeignKey("tblTrafficSignDataset.id"))
    path = db.Column(db.String(255))
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'version': self.version,
            'pre': self.pre,
            'recall': self.recall,
            'f1_score': self.f1_score,
            'is_active': self.is_active,
            'sample_quantity': self.sample_quantity,
            'dataset_id': self.dataset_id,
            'path': self.path
        }
