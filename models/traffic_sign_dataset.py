from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class TrafficSignDataset(db.Model):
    __tablename__ = "tblTrafficSignDataset"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    cloudPath = db.Column(db.String(255))
    yaml_path = db.Column(db.String(255))
