from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from typing import Optional
from database import SessionLocal, engine
from pydantic import BaseModel
import crud
import utils
import models
from models import URL, Base
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


# Create database tables
models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

# Dependency for accessing the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class URLShortenRequest(BaseModel):
    url: str
    custom_path: Optional[str] = None

def serialize_url(url):
    return {
        "id": url.id,
        "long_url": url.long_url,
        "short_path": url.short_path,
    }



@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
    

@app.post("/shorten/", response_model=dict)
def shorten_url(url_data: URLShortenRequest, db: Session = Depends(get_db)):
    # Validate URL
    if not utils.is_valid_url(url_data.url):
        raise HTTPException(status_code=400, detail="Invalid URL")

    # Check if custom path already exists
    if url_data.custom_path and crud.get_url_by_short_path(db, url_data.custom_path):
        raise HTTPException(status_code=400, detail="Custom path already exists")

    # Generate short URL
    short_url = utils.generate_short_url(url_data.url, url_data.custom_path)

    # Save to database
    new_url = crud.create_url(db, short_url)
    
    # Serialize the URL object
    serialized_url = serialize_url(new_url)
    
    return serialized_url

@app.get("/{short_path}/")
def redirect_short_url(short_path: str, db: Session = Depends(get_db)):
    url = crud.get_url_by_short_path(db, short_path)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    return RedirectResponse(url.long_url)

@app.get("/analytics/{short_path}/")
def get_url_analytics(short_path: str, db: Session = Depends(get_db)):
    url = crud.get_url_by_short_path(db, short_path)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    # Get analytics data (e.g., click count, unique visitors) from database
    # Implement your analytics logic here
    return {"analytics": "data"}

@app.get("/history/")
def get_user_link_history(db: Session = Depends(get_db)):
    # Get link history for the current user (if you have user authentication)
    # Implement your logic to fetch link history from the database
    return {"history": "data"}

@app.post("/generate_qr/")
def generate_qr_code(url_data: URLShortenRequest):
    # Generate QR code
    qr_code_file = utils.generate_qr_code(url_data.url)
    
    # Return QR code file path
    return {"qr_code_file": qr_code_file}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
