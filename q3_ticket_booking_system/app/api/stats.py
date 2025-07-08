from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/api/booking-system", tags=["statistics"])

@router.get("/stats", response_model=schemas.BookingStats)
def get_booking_stats(db: Session = Depends(get_db)):
    """Get booking statistics (total bookings, events, venues, available tickets)"""
    stats = crud.get_booking_stats(db)
    return stats 