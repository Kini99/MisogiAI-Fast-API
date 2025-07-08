from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import crud, schemas, models

router = APIRouter(prefix="/api/venues", tags=["venues"])

@router.post("/", response_model=schemas.VenueResponse, status_code=status.HTTP_201_CREATED)
def create_venue(venue: schemas.VenueCreate, db: Session = Depends(get_db)):
    """Create a new venue"""
    return crud.create_venue(db=db, venue=venue)

@router.get("/", response_model=List[schemas.VenueResponse])
def get_venues(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all venues"""
    venues = crud.get_venues(db, skip=skip, limit=limit)
    return venues

@router.get("/{venue_id}", response_model=schemas.VenueResponse)
def get_venue(venue_id: int, db: Session = Depends(get_db)):
    """Get a specific venue by ID"""
    venue = crud.get_venue(db, venue_id=venue_id)
    if venue is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venue not found"
        )
    return venue

@router.put("/{venue_id}", response_model=schemas.VenueResponse)
def update_venue(venue_id: int, venue: schemas.VenueUpdate, db: Session = Depends(get_db)):
    """Update a venue"""
    db_venue = crud.update_venue(db=db, venue_id=venue_id, venue=venue)
    if db_venue is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venue not found"
        )
    return db_venue

@router.delete("/{venue_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_venue(venue_id: int, db: Session = Depends(get_db)):
    """Delete a venue"""
    success = crud.delete_venue(db=db, venue_id=venue_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venue not found"
        )

@router.get("/{venue_id}/events", response_model=List[schemas.EventResponse])
def get_venue_events(venue_id: int, db: Session = Depends(get_db)):
    """Get all events at a specific venue"""
    # Check if venue exists
    venue = crud.get_venue(db, venue_id)
    if not venue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venue not found"
        )
    
    events = crud.get_venue_events(db, venue_id)
    return events

@router.get("/{venue_id}/occupancy", response_model=schemas.VenueOccupancy)
def get_venue_occupancy(venue_id: int, db: Session = Depends(get_db)):
    """Get venue occupancy statistics"""
    occupancy = crud.get_venue_occupancy(db, venue_id)
    if not occupancy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venue not found"
        )
    return occupancy 