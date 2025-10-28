from datetime import datetime
import uuid
from . import db

class ArtisanShowcaseMedia(db.Model):
    __tablename__ = "artisan_showcase_media"
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    artisan_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    url = db.Column(db.Text, nullable=False)
    media_type = db.Column(db.String(20))
    caption = db.Column(db.Text)
    position = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ArtisanSocial(db.Model):
    __tablename__ = "artisan_socials"
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    artisan_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    platform = db.Column(db.String(50))
    handle = db.Column(db.String(255))
    url = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)