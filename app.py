from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse, FileResponse
from sqlalchemy.orm import Session

from db import Base, engine, get_db
from models import URL, URLRequest

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastURL API",
    description="A simple URL Shortener built using FastAPI and PostgreSQL",
    version="1.0.0"
)


# ---------------------------------------
# Home Page
# ---------------------------------------
@app.get("/", include_in_schema=False)
def home():
    return FileResponse("index.html")


@app.get("/health")
def health():
    return {
        "status": "running",
        "message": "FastURL API is working"
    }



@app.post("/shorten")
def create_short_url(
    request: URLRequest,
    db: Session = Depends(get_db)
):
    url = URL.shorten_url(
        db=db,
        original_url=str(request.url)
    )

    return {
        "message": "URL shortened successfully.",
        "original_url": url.original_url,
        "short_code": url.short_code,
        "short_url": f"http://127.0.0.1:8000/{url.short_code}"
    }

@app.get("/{short_code}")
def redirect_to_original_url(
    short_code: str,
    db: Session = Depends(get_db)
):
    url = URL.get_by_short_code(
        db=db,
        short_code=short_code
    )

    if url is None:
        raise HTTPException(
            status_code=404,
            detail="Short URL not found."
        )

    url.increment_clicks(db)

    return RedirectResponse(
        url=url.original_url,
        status_code=307
    )

# ---------------------------------------
@app.get("/stats/{short_code}")
def get_statistics(
    short_code: str,
    db: Session = Depends(get_db)
):
    url = URL.get_by_short_code(
        db=db,
        short_code=short_code
    )

    if url is None:
        raise HTTPException(
            status_code=404,
            detail="Short URL not found."
        )

    return {
        "original_url": url.original_url,
        "short_code": url.short_code,
        "short_url": f"http://127.0.0.1:8000/{url.short_code}",
        "clicks": url.clicks
    }