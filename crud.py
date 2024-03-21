from sqlalchemy.orm import Session
import models

def create_url(db: Session, url: models.URL) -> models.URL:
    db.add(url)
    db.commit()
    db.refresh(url)
    return url

def get_url_by_short_path(db: Session, short_path: str):
    query = db.query(models.URL).filter(models.URL.short_path == short_path)
    return query.first()
