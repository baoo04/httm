from app import db

class DetailTrafficSignSample(db.Model):
    __tablename__ = "tblDetailTrafficSignSample"
    sample_id = db.Column(db.Integer, db.ForeignKey("tblTrafficSignSample.id"), primary_key=True)
    label_id = db.Column(db.Integer, db.ForeignKey("tblTrafficSignLabel.id"), primary_key=True)