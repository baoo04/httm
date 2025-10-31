from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class TrafficSignSample(db.Model):
    __tablename__ = "tblTrafficSignSample"
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(255))
    admin_id = db.Column(db.Integer, db.ForeignKey("tblAdmin.id"))
    dataset_id = db.Column(db.Integer, db.ForeignKey("tblTrafficSignDataset.id"))
