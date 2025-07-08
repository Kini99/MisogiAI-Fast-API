from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import crud, schemas, models

router = APIRouter(prefix="/api/ticket-types", tags=["ticket-types"])

@router.post("/", response_model=schemas.TicketTypeResponse, status_code=status.HTTP_201_CREATED)
def create_ticket_type(ticket_type: schemas.TicketTypeCreate, db: Session = Depends(get_db)):
    """Create a new ticket type"""
    return crud.create_ticket_type(db=db, ticket_type=ticket_type)

@router.get("/", response_model=List[schemas.TicketTypeResponse])
def get_ticket_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all ticket types"""
    ticket_types = crud.get_ticket_types(db, skip=skip, limit=limit)
    return ticket_types

@router.get("/{ticket_type_id}", response_model=schemas.TicketTypeResponse)
def get_ticket_type(ticket_type_id: int, db: Session = Depends(get_db)):
    """Get a specific ticket type by ID"""
    ticket_type = crud.get_ticket_type(db, ticket_type_id=ticket_type_id)
    if ticket_type is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket type not found"
        )
    return ticket_type

@router.put("/{ticket_type_id}", response_model=schemas.TicketTypeResponse)
def update_ticket_type(ticket_type_id: int, ticket_type: schemas.TicketTypeUpdate, db: Session = Depends(get_db)):
    """Update a ticket type"""
    db_ticket_type = crud.update_ticket_type(db=db, ticket_type_id=ticket_type_id, ticket_type=ticket_type)
    if db_ticket_type is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket type not found"
        )
    return db_ticket_type

@router.delete("/{ticket_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket_type(ticket_type_id: int, db: Session = Depends(get_db)):
    """Delete a ticket type"""
    success = crud.delete_ticket_type(db=db, ticket_type_id=ticket_type_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket type not found"
        )

@router.get("/{ticket_type_id}/bookings", response_model=List[schemas.BookingResponse])
def get_ticket_type_bookings(ticket_type_id: int, db: Session = Depends(get_db)):
    """Get all bookings for a specific ticket type"""
    # Check if ticket type exists
    ticket_type = crud.get_ticket_type(db, ticket_type_id)
    if not ticket_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket type not found"
        )
    
    bookings = crud.get_ticket_type_bookings(db, ticket_type_id)
    return bookings 