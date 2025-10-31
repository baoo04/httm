from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class TrafficSignDataset(db.Model):
    __tablename__ = "tblTrafficSignDataset"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    cloud_path = db.Column(db.String(255))
