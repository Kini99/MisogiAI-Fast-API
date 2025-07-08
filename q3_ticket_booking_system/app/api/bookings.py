from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app import crud, schemas, models

router = APIRouter(prefix="/api/bookings", tags=["bookings"])

@router.post("/", response_model=schemas.BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    """Create a new booking"""
    # Validate event exists
    event = crud.get_event(db, booking.event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    # Validate venue exists
    venue = crud.get_venue(db, booking.venue_id)
    if not venue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venue not found"
        )
    
    # Validate ticket type exists
    ticket_type = crud.get_ticket_type(db, booking.ticket_type_id)
    if not ticket_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket type not found"
        )
    
    # Check if venue matches event venue
    if event.venue_id != booking.venue_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Venue does not match event venue"
        )
    
    # Check availability
    available_tickets = crud.get_available_tickets(db, booking.event_id)
    if available_tickets["available_tickets"] < booking.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Not enough tickets available. Only {available_tickets['available_tickets']} tickets left."
        )
    
    try:
        return crud.create_booking(db=db, booking=booking)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[schemas.BookingResponse])
def get_bookings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all bookings with event, venue, and ticket type details"""
    bookings = crud.get_bookings(db, skip=skip, limit=limit)
    return bookings

@router.get("/search/", response_model=List[schemas.BookingResponse])
def search_bookings(
    event_name: Optional[str] = Query(None, description="Search by event name"),
    venue_name: Optional[str] = Query(None, description="Search by venue name"),
    ticket_type: Optional[str] = Query(None, description="Search by ticket type"),
    status: Optional[models.BookingStatus] = Query(None, description="Filter by booking status"),
    db: Session = Depends(get_db)
):
    """Search bookings by event name, venue, and/or ticket type"""
    bookings = crud.search_bookings(
        db=db,
        event_name=event_name,
        venue_name=venue_name,
        ticket_type=ticket_type,
        status=status
    )
    return bookings

@router.get("/{booking_id}", response_model=schemas.BookingResponse)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    """Get a specific booking by ID"""
    booking = crud.get_booking(db, booking_id=booking_id)
    if booking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    return booking

@router.put("/{booking_id}", response_model=schemas.BookingResponse)
def update_booking(booking_id: int, booking: schemas.BookingUpdate, db: Session = Depends(get_db)):
    """Update booking details"""
    db_booking = crud.update_booking(db=db, booking_id=booking_id, booking=booking)
    if db_booking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    return db_booking

@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    """Cancel a booking"""
    success = crud.delete_booking(db=db, booking_id=booking_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )

@router.patch("/{booking_id}/status", response_model=schemas.BookingResponse)
def update_booking_status(booking_id: int, status_update: schemas.BookingStatusUpdate, db: Session = Depends(get_db)):
    """Update booking status (confirmed, cancelled, pending)"""
    db_booking = crud.update_booking_status(db=db, booking_id=booking_id, status=status_update.status)
    if db_booking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    return db_booking 