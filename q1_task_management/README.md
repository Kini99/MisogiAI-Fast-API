# Task Management API

A simple FastAPI application with in-memory storage for task management, featuring a clean web UI.

## Features

- **RESTful API**: Complete CRUD operations for tasks
- **Web UI**: Simple and intuitive interface for task management
- **In-memory Storage**: Fast and lightweight storage solution
- **Error Handling**: Proper HTTP status codes and error responses

## API Endpoints

- `GET /tasks` - Fetch all tasks
- `POST /tasks` - Create a new task
- `PUT /tasks/{task_id}` - Update an existing task
- `DELETE /tasks/{task_id}` - Delete a task

## Web UI Features

- Display all tasks in a clean list format
- Form to create new tasks
- Toggle buttons to mark tasks as complete/incomplete
- Delete buttons for each task
- Responsive design

## Requirements

- Python 3.11+
- FastAPI
- Uvicorn
- Jinja2

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd q1
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the server:
```bash
uvicorn main:app --reload
```

2. Open your browser and navigate to:
   - Web UI: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Usage

### Web Interface
- Visit http://localhost:8000 to access the task management interface
- Add new tasks using the form at the top
- Toggle task completion status by clicking the checkbox
- Delete tasks using the delete button

### API Usage

#### Get all tasks
```bash
curl http://localhost:8000/tasks
```

#### Create a new task
```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "New Task", "description": "Task description"}'
```

#### Update a task
```bash
curl -X PUT http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Task", "description": "Updated description", "completed": true}'
```

#### Delete a task
```bash
curl -X DELETE http://localhost:8000/tasks/1
```

## Project Structure

```
q1/
├── main.py              # FastAPI application
├── models.py            # Pydantic models
├── templates/           # HTML templates
│   └── index.html      # Main UI template
├── static/             # Static files
│   └── style.css       # CSS styles
├── requirements.txt    # Python dependencies
├── .gitignore         # Git ignore file
└── README.md          # This file
```

## Error Handling

The application includes proper error handling for:
- Invalid task IDs (404 Not Found)
- Malformed request data (422 Unprocessable Entity)
- Missing required fields (400 Bad Request)

## Development

The application uses:
- **FastAPI** for the web framework
- **Pydantic** for data validation
- **Jinja2** for HTML templating
- **Uvicorn** as the ASGI server

## License

This project is open source and available under the MIT License. 