from app import db

class TrafficSignLabel(db.Model):
    __tablename__ = "tblTrafficSignLabel"
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer)
    title = db.Column(db.String(255))

