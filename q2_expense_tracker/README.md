# Expense Tracker

A modern FastAPI application for tracking personal expenses with a beautiful web interface and RESTful API.

## Features

- **📊 Expense Management**: Add, view, update, and delete expenses
- **🏷️ Category Filtering**: Filter expenses by predefined categories
- **📈 Analytics**: View total expenses and breakdown by category
- **📅 Date Filtering**: Filter expenses by date range
- **💾 SQLite Database**: Lightweight database with automatic setup
- **🎨 Modern UI**: Responsive web interface with beautiful design
- **🔒 Data Validation**: Input validation and error handling
- **📱 Mobile Friendly**: Responsive design for all devices

## Tech Stack

- **Backend**: FastAPI (Python 3.11)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML, CSS, JavaScript with Jinja2 templates
- **Validation**: Pydantic models with custom validators

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd q2
   ```

2. **Create a virtual environment**
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Web UI: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## API Endpoints

### REST API

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/expenses` | Get all expenses (with optional date filtering) |
| `POST` | `/api/expenses` | Create a new expense |
| `PUT` | `/api/expenses/{id}` | Update an existing expense |
| `DELETE` | `/api/expenses/{id}` | Delete an expense |
| `GET` | `/api/expenses/category/{category}` | Get expenses by category |
| `GET` | `/api/expenses/total` | Get total expenses and category breakdown |

### Web UI Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Main expense tracking interface |
| `POST` | `/expenses/add` | Add new expense via web form |
| `POST` | `/expenses/{id}/delete` | Delete expense via web interface |
| `GET` | `/expenses/filter` | Filter expenses by category |

## Usage Examples

### Adding an Expense via API

```bash
curl -X POST "http://localhost:8000/api/expenses" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Lunch",
    "amount": 15.50,
    "category": "Food",
    "date": "2025-01-20"
  }'
```

### Getting Expenses with Date Filtering

```bash
curl "http://localhost:8000/api/expenses?start_date=2025-01-01&end_date=2025-01-31"
```

### Getting Total Expenses

```bash
curl "http://localhost:8000/api/expenses/total"
```

## Data Models

### Expense Model

```python
{
    "id": 1,
    "description": "Lunch",
    "amount": 15.50,
    "category": "Food",
    "date": "2025-01-20",
    "created_at": "2025-01-20T10:30:00"
}
```

### Valid Categories

- Food
- Transport
- Entertainment
- Shopping
- Bills
- Other

## Database Schema

The application automatically creates the following table:

```sql
CREATE TABLE expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description VARCHAR NOT NULL,
    amount FLOAT NOT NULL,
    category VARCHAR NOT NULL,
    date DATE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Features in Detail

### Data Validation

- **Amount**: Must be positive (> 0)
- **Category**: Must be from predefined list
- **Date**: Must be valid date format
- **Description**: Required field

### Query Parameters

- **Date Range Filtering**: Use `start_date` and `end_date` parameters
  - Example: `?start_date=2025-01-01&end_date=2025-01-31`

### Error Handling

- Proper HTTP status codes (400, 404, 500)
- Descriptive error messages
- Form validation with user feedback

### Sample Data

The application includes sample data for testing:
- Lunch ($15.50) - Food category
- Gas ($45.00) - Transport category
- Movie tickets ($25.00) - Entertainment category
- Groceries ($75.30) - Food category
- Electricity bill ($120.00) - Bills category

## Development

### Project Structure

```
q2/
├── app.py              # Main FastAPI application
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── .gitignore         # Git ignore rules
├── templates/         # HTML templates
│   └── index.html     # Main UI template
└── expenses.db        # SQLite database (created automatically)
```

### Running in Development Mode

```bash
# Install development dependencies
pip install -r requirements.txt

# Run with auto-reload
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Database Operations

The application uses SQLAlchemy for database operations:
- Automatic table creation on startup
- Proper session management
- CRUD operations with error handling
- Connection pooling

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions, please create an issue in the repository. 