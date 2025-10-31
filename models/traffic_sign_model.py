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
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
