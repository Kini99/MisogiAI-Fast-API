from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, and_, or_
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime

from app import models, schemas

# Venue CRUD operations
def create_venue(db: Session, venue: schemas.VenueCreate) -> models.Venue:
    db_venue = models.Venue(**venue.dict())
    db.add(db_venue)
    db.commit()
    db.refresh(db_venue)
    return db_venue

def get_venues(db: Session, skip: int = 0, limit: int = 100) -> List[models.Venue]:
    return db.query(models.Venue).offset(skip).limit(limit).all()

def get_venue(db: Session, venue_id: int) -> Optional[models.Venue]:
    return db.query(models.Venue).filter(models.Venue.id == venue_id).first()

def update_venue(db: Session, venue_id: int, venue: schemas.VenueUpdate) -> Optional[models.Venue]:
    db_venue = get_venue(db, venue_id)
    if db_venue:
        update_data = venue.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_venue, field, value)
        db.commit()
        db.refresh(db_venue)
    return db_venue

def delete_venue(db: Session, venue_id: int) -> bool:
    db_venue = get_venue(db, venue_id)
    if db_venue:
        db.delete(db_venue)
        db.commit()
        return True
    return False

def get_venue_events(db: Session, venue_id: int) -> List[models.Event]:
    return db.query(models.Event).filter(models.Event.venue_id == venue_id).all()

def get_venue_occupancy(db: Session, venue_id: int) -> Dict[str, Any]:
    venue = get_venue(db, venue_id)
    if not venue:
        return None
    
    # Get total events at this venue
    total_events = db.query(models.Event).filter(models.Event.venue_id == venue_id).count()
    
    # Get total bookings for this venue
    total_booked = db.query(func.sum(models.Booking.quantity)).filter(
        models.Booking.venue_id == venue_id,
        models.Booking.status == models.BookingStatus.CONFIRMED
    ).scalar() or 0
    
    # Calculate occupancy rate
    occupancy_rate = (total_booked / venue.capacity * 100) if venue.capacity > 0 else 0
    
    return {
        "venue_id": venue.id,
        "venue_name": venue.name,
        "total_capacity": venue.capacity,
        "total_booked": total_booked,
        "occupancy_rate": round(occupancy_rate, 2),
        "total_events": total_events
    }

# Event CRUD operations
def create_event(db: Session, event: schemas.EventCreate) -> models.Event:
    db_event = models.Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_events(db: Session, skip: int = 0, limit: int = 100) -> List[models.Event]:
    return db.query(models.Event).options(joinedload(models.Event.venue)).offset(skip).limit(limit).all()

def get_event(db: Session, event_id: int) -> Optional[models.Event]:
    return db.query(models.Event).options(joinedload(models.Event.venue)).filter(models.Event.id == event_id).first()

def update_event(db: Session, event_id: int, event: schemas.EventUpdate) -> Optional[models.Event]:
    db_event = get_event(db, event_id)
    if db_event:
        update_data = event.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_event, field, value)
        db.commit()
        db.refresh(db_event)
    return db_event

def delete_event(db: Session, event_id: int) -> bool:
    db_event = get_event(db, event_id)
    if db_event:
        db.delete(db_event)
        db.commit()
        return True
    return False

def get_event_bookings(db: Session, event_id: int) -> List[models.Booking]:
    return db.query(models.Booking).options(
        joinedload(models.Booking.event),
        joinedload(models.Booking.venue),
        joinedload(models.Booking.ticket_type)
    ).filter(models.Booking.event_id == event_id).all()

def get_event_revenue(db: Session, event_id: int) -> Dict[str, Any]:
    event = get_event(db, event_id)
    if not event:
        return None
    
    # Get total revenue and bookings for this event
    result = db.query(
        func.sum(models.Booking.total_amount).label('total_revenue'),
        func.count(models.Booking.id).label('total_bookings'),
        func.avg(models.Booking.total_amount / models.Booking.quantity).label('avg_ticket_price')
    ).filter(
        models.Booking.event_id == event_id,
        models.Booking.status == models.BookingStatus.CONFIRMED
    ).first()
    
    return {
        "event_id": event.id,
        "event_name": event.name,
        "total_revenue": result.total_revenue or 0,
        "total_bookings": result.total_bookings or 0,
        "average_ticket_price": round(result.avg_ticket_price or 0, 2)
    }

def get_available_tickets(db: Session, event_id: int) -> Dict[str, Any]:
    event = get_event(db, event_id)
    if not event:
        return None
    
    # Get total booked tickets for this event
    total_booked = db.query(func.sum(models.Booking.quantity)).filter(
        models.Booking.event_id == event_id,
        models.Booking.status == models.BookingStatus.CONFIRMED
    ).scalar() or 0
    
    available_tickets = event.capacity - total_booked
    
    # Get ticket types with their availability
    ticket_types = db.query(models.TicketType).all()
    ticket_types_available = []
    
    for ticket_type in ticket_types:
        booked_for_type = db.query(func.sum(models.Booking.quantity)).filter(
            models.Booking.event_id == event_id,
            models.Booking.ticket_type_id == ticket_type.id,
            models.Booking.status == models.BookingStatus.CONFIRMED
        ).scalar() or 0
        
        ticket_types_available.append({
            "ticket_type_id": ticket_type.id,
            "ticket_type_name": ticket_type.name,
            "price": ticket_type.price,
            "booked": booked_for_type,
            "available": available_tickets  # Simplified - in real app, you'd track per ticket type
        })
    
    return {
        "event_id": event.id,
        "event_name": event.name,
        "total_capacity": event.capacity,
        "booked_tickets": total_booked,
        "available_tickets": available_tickets,
        "ticket_types_available": ticket_types_available
    }

# Ticket Type CRUD operations
def create_ticket_type(db: Session, ticket_type: schemas.TicketTypeCreate) -> models.TicketType:
    db_ticket_type = models.TicketType(**ticket_type.dict())
    db.add(db_ticket_type)
    db.commit()
    db.refresh(db_ticket_type)
    return db_ticket_type

def get_ticket_types(db: Session, skip: int = 0, limit: int = 100) -> List[models.TicketType]:
    return db.query(models.TicketType).offset(skip).limit(limit).all()

def get_ticket_type(db: Session, ticket_type_id: int) -> Optional[models.TicketType]:
    return db.query(models.TicketType).filter(models.TicketType.id == ticket_type_id).first()

def update_ticket_type(db: Session, ticket_type_id: int, ticket_type: schemas.TicketTypeUpdate) -> Optional[models.TicketType]:
    db_ticket_type = get_ticket_type(db, ticket_type_id)
    if db_ticket_type:
        update_data = ticket_type.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_ticket_type, field, value)
        db.commit()
        db.refresh(db_ticket_type)
    return db_ticket_type

def delete_ticket_type(db: Session, ticket_type_id: int) -> bool:
    db_ticket_type = get_ticket_type(db, ticket_type_id)
    if db_ticket_type:
        db.delete(db_ticket_type)
        db.commit()
        return True
    return False

def get_ticket_type_bookings(db: Session, ticket_type_id: int) -> List[models.Booking]:
    return db.query(models.Booking).options(
        joinedload(models.Booking.event),
        joinedload(models.Booking.venue),
        joinedload(models.Booking.ticket_type)
    ).filter(models.Booking.ticket_type_id == ticket_type_id).all()

# Booking CRUD operations
def create_booking(db: Session, booking: schemas.BookingCreate) -> models.Booking:
    # Get ticket type to calculate total amount
    ticket_type = get_ticket_type(db, booking.ticket_type_id)
    if not ticket_type:
        raise ValueError("Invalid ticket type")
    
    # Calculate total amount
    total_amount = ticket_type.price * booking.quantity
    
    # Generate unique booking code
    booking_code = f"BK-{uuid.uuid4().hex[:8].upper()}"
    
    # Create booking
    db_booking = models.Booking(
        **booking.dict(),
        total_amount=total_amount,
        booking_code=booking_code
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

def get_bookings(db: Session, skip: int = 0, limit: int = 100) -> List[models.Booking]:
    return db.query(models.Booking).options(
        joinedload(models.Booking.event),
        joinedload(models.Booking.venue),
        joinedload(models.Booking.ticket_type)
    ).offset(skip).limit(limit).all()

def get_booking(db: Session, booking_id: int) -> Optional[models.Booking]:
    return db.query(models.Booking).options(
        joinedload(models.Booking.event),
        joinedload(models.Booking.venue),
        joinedload(models.Booking.ticket_type)
    ).filter(models.Booking.id == booking_id).first()

def update_booking(db: Session, booking_id: int, booking: schemas.BookingUpdate) -> Optional[models.Booking]:
    db_booking = get_booking(db, booking_id)
    if db_booking:
        update_data = booking.dict(exclude_unset=True)
        
        # If quantity is updated, recalculate total amount
        if 'quantity' in update_data:
            ticket_type = get_ticket_type(db, db_booking.ticket_type_id)
            update_data['total_amount'] = ticket_type.price * update_data['quantity']
        
        for field, value in update_data.items():
            setattr(db_booking, field, value)
        db.commit()
        db.refresh(db_booking)
    return db_booking

def update_booking_status(db: Session, booking_id: int, status: models.BookingStatus) -> Optional[models.Booking]:
    db_booking = get_booking(db, booking_id)
    if db_booking:
        db_booking.status = status
        db.commit()
        db.refresh(db_booking)
    return db_booking

def delete_booking(db: Session, booking_id: int) -> bool:
    db_booking = get_booking(db, booking_id)
    if db_booking:
        db.delete(db_booking)
        db.commit()
        return True
    return False

def search_bookings(db: Session, event_name: str = None, venue_name: str = None, 
                   ticket_type: str = None, status: models.BookingStatus = None) -> List[models.Booking]:
    query = db.query(models.Booking).options(
        joinedload(models.Booking.event),
        joinedload(models.Booking.venue),
        joinedload(models.Booking.ticket_type)
    )
    
    if event_name:
        query = query.join(models.Event).filter(models.Event.name.ilike(f"%{event_name}%"))
    
    if venue_name:
        query = query.join(models.Venue).filter(models.Venue.name.ilike(f"%{venue_name}%"))
    
    if ticket_type:
        query = query.join(models.TicketType).filter(models.TicketType.name.ilike(f"%{ticket_type}%"))
    
    if status:
        query = query.filter(models.Booking.status == status)
    
    return query.all()

def get_booking_stats(db: Session) -> Dict[str, Any]:
    # Get total counts
    total_bookings = db.query(models.Booking).count()
    total_events = db.query(models.Event).count()
    total_venues = db.query(models.Venue).count()
    
    # Get status counts
    confirmed_bookings = db.query(models.Booking).filter(
        models.Booking.status == models.BookingStatus.CONFIRMED
    ).count()
    pending_bookings = db.query(models.Booking).filter(
        models.Booking.status == models.BookingStatus.PENDING
    ).count()
    cancelled_bookings = db.query(models.Booking).filter(
        models.Booking.status == models.BookingStatus.CANCELLED
    ).count()
    
    # Get total revenue
    total_revenue = db.query(func.sum(models.Booking.total_amount)).filter(
        models.Booking.status == models.BookingStatus.CONFIRMED
    ).scalar() or 0
    
    return {
        "total_bookings": total_bookings,
        "total_events": total_events,
        "total_venues": total_venues,
        "total_revenue": total_revenue,
        "confirmed_bookings": confirmed_bookings,
        "pending_bookings": pending_bookings,
        "cancelled_bookings": cancelled_bookings
    } 