from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os

from app.database import engine
from app import models
from app.api import events, venues, ticket_types, bookings, stats

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Ticket Booking Management System",
    description="A comprehensive FastAPI application for managing ticket bookings, events, venues, and ticket types",
    version="1.0.0"
)

# Include API routers
app.include_router(events.router)
app.include_router(venues.router)
app.include_router(ticket_types.router)
app.include_router(bookings.router)
app.include_router(stats.router)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Web interface routes
@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Main dashboard page"""
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/events", response_class=HTMLResponse)
async def events_page(request: Request):
    """Events management page"""
    return templates.TemplateResponse("events.html", {"request": request})

@app.get("/venues", response_class=HTMLResponse)
async def venues_page(request: Request):
    """Venues management page"""
    return templates.TemplateResponse("venues.html", {"request": request})

@app.get("/ticket-types", response_class=HTMLResponse)
async def ticket_types_page(request: Request):
    """Ticket types management page"""
    return templates.TemplateResponse("ticket_types.html", {"request": request})

@app.get("/bookings", response_class=HTMLResponse)
async def bookings_page(request: Request):
    """Bookings management page"""
    return templates.TemplateResponse("bookings.html", {"request": request})

@app.get("/search", response_class=HTMLResponse)
async def search_page(request: Request):
    """Search interface page"""
    return templates.TemplateResponse("search.html", {"request": request})

@app.get("/calendar", response_class=HTMLResponse)
async def calendar_page(request: Request):
    """Calendar view page"""
    return templates.TemplateResponse("calendar.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 