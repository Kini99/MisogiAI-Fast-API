#!/usr/bin/env python3
"""
Test script for the Ticket Booking Management System API
This script demonstrates the core functionality by creating sample data and testing the API endpoints.
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

def test_api():
    print("🚀 Testing Ticket Booking Management System API")
    print("=" * 50)
    
    # Test 1: Create Venues
    print("\n1. Creating Venues...")
    venues = [
        {
            "name": "Grand Concert Hall",
            "address": "123 Music Street, Downtown",
            "capacity": 1000
        },
        {
            "name": "Intimate Theater",
            "address": "456 Arts Avenue, Midtown",
            "capacity": 200
        },
        {
            "name": "Stadium Arena",
            "address": "789 Sports Boulevard, Uptown",
            "capacity": 5000
        }
    ]
    
    venue_ids = []
    for venue in venues:
        response = requests.post(f"{BASE_URL}/api/venues/", json=venue)
        if response.status_code == 201:
            venue_data = response.json()
            venue_ids.append(venue_data["id"])
            print(f"✅ Created venue: {venue_data['name']} (ID: {venue_data['id']})")
        else:
            print(f"❌ Failed to create venue: {venue['name']} - {response.text}")
    
    # Test 2: Create Ticket Types
    print("\n2. Creating Ticket Types...")
    ticket_types = [
        {
            "name": "VIP",
            "price": 150.00,
            "description": "Premium seating with exclusive amenities"
        },
        {
            "name": "Standard",
            "price": 75.00,
            "description": "Regular seating with good view"
        },
        {
            "name": "Economy",
            "price": 35.00,
            "description": "Basic seating at affordable price"
        }
    ]
    
    ticket_type_ids = []
    for ticket_type in ticket_types:
        response = requests.post(f"{BASE_URL}/api/ticket-types/", json=ticket_type)
        if response.status_code == 201:
            ticket_data = response.json()
            ticket_type_ids.append(ticket_data["id"])
            print(f"✅ Created ticket type: {ticket_data['name']} - ${ticket_data['price']} (ID: {ticket_data['id']})")
        else:
            print(f"❌ Failed to create ticket type: {ticket_type['name']} - {response.text}")
    
    # Test 3: Create Events
    print("\n3. Creating Events...")
    events = [
        {
            "name": "Rock Concert 2024",
            "description": "Amazing rock concert featuring top artists",
            "date": (datetime.now() + timedelta(days=30)).isoformat(),
            "venue_id": venue_ids[0],
            "capacity": 800
        },
        {
            "name": "Jazz Night",
            "description": "Intimate jazz performance",
            "date": (datetime.now() + timedelta(days=15)).isoformat(),
            "venue_id": venue_ids[1],
            "capacity": 150
        },
        {
            "name": "Sports Championship",
            "description": "Annual sports championship event",
            "date": (datetime.now() + timedelta(days=45)).isoformat(),
            "venue_id": venue_ids[2],
            "capacity": 4000
        }
    ]
    
    event_ids = []
    for event in events:
        response = requests.post(f"{BASE_URL}/api/events/", json=event)
        if response.status_code == 201:
            event_data = response.json()
            event_ids.append(event_data["id"])
            print(f"✅ Created event: {event_data['name']} (ID: {event_data['id']})")
        else:
            print(f"❌ Failed to create event: {event['name']} - {response.text}")
    
    # Test 4: Create Bookings
    print("\n4. Creating Bookings...")
    bookings = [
        {
            "event_id": event_ids[0],
            "venue_id": venue_ids[0],
            "ticket_type_id": ticket_type_ids[0],
            "customer_name": "John Doe",
            "customer_email": "john@example.com",
            "quantity": 2
        },
        {
            "event_id": event_ids[0],
            "venue_id": venue_ids[0],
            "ticket_type_id": ticket_type_ids[1],
            "customer_name": "Jane Smith",
            "customer_email": "jane@example.com",
            "quantity": 1
        },
        {
            "event_id": event_ids[1],
            "venue_id": venue_ids[1],
            "ticket_type_id": ticket_type_ids[2],
            "customer_name": "Bob Johnson",
            "customer_email": "bob@example.com",
            "quantity": 3
        },
        {
            "event_id": event_ids[2],
            "venue_id": venue_ids[2],
            "ticket_type_id": ticket_type_ids[1],
            "customer_name": "Alice Brown",
            "customer_email": "alice@example.com",
            "quantity": 4
        }
    ]
    
    booking_ids = []
    for booking in bookings:
        response = requests.post(f"{BASE_URL}/api/bookings/", json=booking)
        if response.status_code == 201:
            booking_data = response.json()
            booking_ids.append(booking_data["id"])
            print(f"✅ Created booking: {booking_data['customer_name']} - {booking_data['booking_code']} (ID: {booking_data['id']})")
        else:
            print(f"❌ Failed to create booking for {booking['customer_name']}: {response.text}")
    
    # Test 5: Get Statistics
    print("\n5. Getting System Statistics...")
    response = requests.get(f"{BASE_URL}/api/booking-system/stats")
    if response.status_code == 200:
        stats = response.json()
        print(f"✅ Total Bookings: {stats['total_bookings']}")
        print(f"✅ Total Events: {stats['total_events']}")
        print(f"✅ Total Venues: {stats['total_venues']}")
        print(f"✅ Total Revenue: ${stats['total_revenue']:.2f}")
        print(f"✅ Confirmed Bookings: {stats['confirmed_bookings']}")
        print(f"✅ Pending Bookings: {stats['pending_bookings']}")
        print(f"✅ Cancelled Bookings: {stats['cancelled_bookings']}")
    
    # Test 6: Get Event Revenue
    print(f"\n6. Getting Revenue for Event ID {event_ids[0]}...")
    response = requests.get(f"{BASE_URL}/api/events/{event_ids[0]}/revenue")
    if response.status_code == 200:
        revenue = response.json()
        print(f"✅ Event Revenue: ${revenue['total_revenue']:.2f}")
        print(f"✅ Total Bookings: {revenue['total_bookings']}")
        print(f"✅ Average Ticket Price: ${revenue['average_ticket_price']:.2f}")
    
    # Test 7: Get Venue Occupancy
    print(f"\n7. Getting Occupancy for Venue ID {venue_ids[0]}...")
    response = requests.get(f"{BASE_URL}/api/venues/{venue_ids[0]}/occupancy")
    if response.status_code == 200:
        occupancy = response.json()
        print(f"✅ Total Capacity: {occupancy['total_capacity']}")
        print(f"✅ Total Booked: {occupancy['total_booked']}")
        print(f"✅ Occupancy Rate: {occupancy['occupancy_rate']}%")
        print(f"✅ Total Events: {occupancy['total_events']}")
    
    # Test 8: Search Bookings
    print("\n8. Searching Bookings...")
    response = requests.get(f"{BASE_URL}/api/bookings/search?event_name=Rock")
    if response.status_code == 200:
        search_results = response.json()
        print(f"✅ Found {len(search_results)} bookings for 'Rock' events")
    
    # Test 9: Update Booking Status
    if booking_ids:
        print(f"\n9. Updating Booking Status for ID {booking_ids[0]}...")
        response = requests.patch(f"{BASE_URL}/api/bookings/{booking_ids[0]}/status", 
                                json={"status": "confirmed"})
        if response.status_code == 200:
            print("✅ Booking status updated to confirmed")
    
    print("\n" + "=" * 50)
    print("🎉 API Testing Completed Successfully!")
    print(f"🌐 Web Interface: http://localhost:8000")
    print(f"📚 API Documentation: http://localhost:8000/docs")
    print(f"📖 Alternative Docs: http://localhost:8000/redoc")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the server. Make sure the application is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}") 