from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import crud, schemas, models

router = APIRouter(prefix="/api/events", tags=["events"])

@router.post("/", response_model=schemas.EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    """Create a new event"""
    # Validate venue exists
    venue = crud.get_venue(db, event.venue_id)
    if not venue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venue not found"
        )
    
    return crud.create_event(db=db, event=event)

@router.get("/", response_model=List[schemas.EventResponse])
def get_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all events"""
    events = crud.get_events(db, skip=skip, limit=limit)
    return events

@router.get("/{event_id}", response_model=schemas.EventResponse)
def get_event(event_id: int, db: Session = Depends(get_db)):
    """Get a specific event by ID"""
    event = crud.get_event(db, event_id=event_id)
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return event

@router.put("/{event_id}", response_model=schemas.EventResponse)
def update_event(event_id: int, event: schemas.EventUpdate, db: Session = Depends(get_db)):
    """Update an event"""
    db_event = crud.update_event(db=db, event_id=event_id, event=event)
    if db_event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return db_event

@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    """Delete an event"""
    success = crud.delete_event(db=db, event_id=event_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

@router.get("/{event_id}/bookings", response_model=List[schemas.BookingResponse])
def get_event_bookings(event_id: int, db: Session = Depends(get_db)):
    """Get all bookings for a specific event"""
    # Check if event exists
    event = crud.get_event(db, event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    bookings = crud.get_event_bookings(db, event_id)
    return bookings

@router.get("/{event_id}/available-tickets", response_model=schemas.AvailableTickets)
def get_available_tickets(event_id: int, db: Session = Depends(get_db)):
    """Get available tickets for an event"""
    available_tickets = crud.get_available_tickets(db, event_id)
    if not available_tickets:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return available_tickets

@router.get("/{event_id}/revenue", response_model=schemas.EventRevenue)
def get_event_revenue(event_id: int, db: Session = Depends(get_db)):
    """Calculate total revenue for a specific event"""
    revenue = crud.get_event_revenue(db, event_id)
    if not revenue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return revenue 