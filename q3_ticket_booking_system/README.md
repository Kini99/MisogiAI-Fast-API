# Ticket Booking Management System

A comprehensive FastAPI application for managing ticket bookings, events, venues, and ticket types with a modern web interface.

## Features

### Core Functionality
- **Event Management**: Create, view, and manage events with booking statistics
- **Venue Management**: Manage venues with capacity tracking and occupancy statistics
- **Ticket Types**: Create different ticket categories (VIP, Standard, Economy) with pricing
- **Booking System**: Complete booking lifecycle with status management
- **Advanced Search**: Filter bookings by event, venue, and ticket type
- **Statistics Dashboard**: Revenue tracking, occupancy rates, and booking analytics

### Database Relationships
- **One-to-Many**: Event → Bookings, Venue → Events, Ticket Type → Bookings
- **Many-to-One**: Bookings → Event, Events → Venue, Bookings → Ticket Type
- **Foreign Key Constraints**: Data integrity with cascade operations
- **Complex Queries**: Join operations for comprehensive data retrieval

### UI Features
- Modern, responsive web interface
- Real-time booking availability
- Interactive statistics dashboard
- Calendar view for events
- Search and filter functionality
- Booking confirmation system

## Setup Instructions

### Prerequisites
- Python 3.11
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd q3
   ```

2. **Create virtual environment**
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize database**
   ```bash
   alembic upgrade head
   ```

5. **Run the application**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Access the application**
   - API Documentation: http://localhost:8000/docs
   - Web Interface: http://localhost:8000
   - Alternative API Docs: http://localhost:8000/redoc

## API Endpoints

### Events
- `POST /events` - Create new event
- `GET /events` - Get all events
- `GET /events/{event_id}/bookings` - Get all bookings for a specific event
- `GET /events/{event_id}/available-tickets` - Get available tickets for an event
- `GET /events/{event_id}/revenue` - Calculate total revenue for a specific event

### Venues
- `POST /venues` - Create new venue
- `GET /venues` - Get all venues
- `GET /venues/{venue_id}/events` - Get all events at a specific venue
- `GET /venues/{venue_id}/occupancy` - Get venue occupancy statistics

### Ticket Types
- `POST /ticket-types` - Create new ticket type
- `GET /ticket-types` - Get all ticket types
- `GET /ticket-types/{type_id}/bookings` - Get all bookings for a specific ticket type

### Bookings
- `POST /bookings` - Create new booking
- `GET /bookings` - Get all bookings with details
- `PUT /bookings/{booking_id}` - Update booking details
- `DELETE /bookings/{booking_id}` - Cancel a booking
- `PATCH /bookings/{booking_id}/status` - Update booking status

### Advanced Queries
- `GET /bookings/search` - Search bookings by criteria
- `GET /booking-system/stats` - Get booking statistics
- `GET /events/{event_id}/revenue` - Calculate event revenue
- `GET /venues/{venue_id}/occupancy` - Get venue occupancy

## Database Schema

### Events
- id (Primary Key)
- name
- description
- date
- venue_id (Foreign Key)
- capacity
- created_at
- updated_at

### Venues
- id (Primary Key)
- name
- address
- capacity
- created_at
- updated_at

### Ticket Types
- id (Primary Key)
- name (VIP, Standard, Economy)
- price
- description
- created_at
- updated_at

### Bookings
- id (Primary Key)
- event_id (Foreign Key)
- venue_id (Foreign Key)
- ticket_type_id (Foreign Key)
- customer_name
- customer_email
- quantity
- total_amount
- status (confirmed, cancelled, pending)
- booking_code
- created_at
- updated_at

## Usage Examples

### Creating an Event
```bash
curl -X POST "http://localhost:8000/events" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Rock Concert 2024",
    "description": "Amazing rock concert",
    "date": "2024-06-15T19:00:00",
    "venue_id": 1,
    "capacity": 1000
  }'
```

### Creating a Booking
```bash
curl -X POST "http://localhost:8000/bookings" \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": 1,
    "venue_id": 1,
    "ticket_type_id": 1,
    "customer_name": "John Doe",
    "customer_email": "john@example.com",
    "quantity": 2
  }'
```

## Project Structure

```
q3/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── .gitignore             # Git ignore file
├── alembic.ini            # Alembic configuration
├── alembic/               # Database migrations
├── app/
│   ├── __init__.py
│   ├── database.py        # Database configuration
│   ├── models.py          # SQLAlchemy models
│   ├── schemas.py         # Pydantic schemas
│   ├── crud.py           # CRUD operations
│   ├── api/
│   │   ├── __init__.py
│   │   ├── events.py      # Event endpoints
│   │   ├── venues.py      # Venue endpoints
│   │   ├── ticket_types.py # Ticket type endpoints
│   │   ├── bookings.py    # Booking endpoints
│   │   └── stats.py       # Statistics endpoints
│   └── templates/         # HTML templates
│       ├── base.html
│       ├── events.html
│       ├── venues.html
│       ├── ticket_types.html
│       ├── bookings.html
│       └── dashboard.html
└── static/               # CSS, JS, and static assets
    ├── css/
    ├── js/
    └── images/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License. 