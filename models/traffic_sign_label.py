from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class TrafficSignLabel(db.Model):
    __tablename__ = "tblTrafficSignLabel"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
