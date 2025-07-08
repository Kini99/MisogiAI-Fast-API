from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime
from app.models import BookingStatus

# Base schemas
class VenueBase(BaseModel):
    name: str
    address: str
    capacity: int

    @validator('capacity')
    def capacity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Capacity must be positive')
        return v

class EventBase(BaseModel):
    name: str
    description: Optional[str] = None
    date: datetime
    venue_id: int
    capacity: int

    @validator('capacity')
    def capacity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Capacity must be positive')
        return v

class TicketTypeBase(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

    @validator('price')
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Price must be positive')
        return v

class BookingBase(BaseModel):
    event_id: int
    venue_id: int
    ticket_type_id: int
    customer_name: str
    customer_email: str
    quantity: int

    @validator('quantity')
    def quantity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Quantity must be positive')
        return v

# Create schemas
class VenueCreate(VenueBase):
    pass

class EventCreate(EventBase):
    pass

class TicketTypeCreate(TicketTypeBase):
    pass

class BookingCreate(BookingBase):
    pass

# Update schemas
class VenueUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    capacity: Optional[int] = None

    @validator('capacity')
    def capacity_must_be_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Capacity must be positive')
        return v

class EventUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    date: Optional[datetime] = None
    venue_id: Optional[int] = None
    capacity: Optional[int] = None

    @validator('capacity')
    def capacity_must_be_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Capacity must be positive')
        return v

class TicketTypeUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None

    @validator('price')
    def price_must_be_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Price must be positive')
        return v

class BookingUpdate(BaseModel):
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    quantity: Optional[int] = None

    @validator('quantity')
    def quantity_must_be_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Quantity must be positive')
        return v

class BookingStatusUpdate(BaseModel):
    status: BookingStatus

# Response schemas
class VenueResponse(VenueBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class EventResponse(EventBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    venue: Optional[VenueResponse] = None

    class Config:
        from_attributes = True

class TicketTypeResponse(TicketTypeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class BookingResponse(BookingBase):
    id: int
    total_amount: float
    status: BookingStatus
    booking_code: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    event: Optional[EventResponse] = None
    venue: Optional[VenueResponse] = None
    ticket_type: Optional[TicketTypeResponse] = None

    class Config:
        from_attributes = True

# List response schemas
class VenueList(BaseModel):
    venues: List[VenueResponse]

class EventList(BaseModel):
    events: List[EventResponse]

class TicketTypeList(BaseModel):
    ticket_types: List[TicketTypeResponse]

class BookingList(BaseModel):
    bookings: List[BookingResponse]

# Statistics schemas
class BookingStats(BaseModel):
    total_bookings: int
    total_events: int
    total_venues: int
    total_revenue: float
    confirmed_bookings: int
    pending_bookings: int
    cancelled_bookings: int

class EventRevenue(BaseModel):
    event_id: int
    event_name: str
    total_revenue: float
    total_bookings: int
    average_ticket_price: float

class VenueOccupancy(BaseModel):
    venue_id: int
    venue_name: str
    total_capacity: int
    total_booked: int
    occupancy_rate: float
    total_events: int

class AvailableTickets(BaseModel):
    event_id: int
    event_name: str
    total_capacity: int
    booked_tickets: int
    available_tickets: int
    ticket_types_available: List[dict]

# Search schemas
class BookingSearch(BaseModel):
    event_name: Optional[str] = None
    venue_name: Optional[str] = None
    ticket_type: Optional[str] = None
    status: Optional[BookingStatus] = None 