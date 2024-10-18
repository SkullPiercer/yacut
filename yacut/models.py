from datetime import datetime

from . import db


class URLMap(db.Model):
    id = db.Colimn(db.Integer, primary_key=True)
    original = db.Column(db.String(128), nullable=False)
    short = db.Column(db.String(128), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)