**DevTrack API**

DevTrack is a Django-based backend API designed for tracking engineering issues. It uses an Object-Oriented Programming (OOP) approach with custom validation and persists data using local JSON storage.

**Features**

OOP Design: Implements a BaseEntity abstract class with Issue and Reporter models.
Inheritance: Specialized issue types (CriticalIssue, LowPriorityIssue) with custom behavior.
JSON Persistence: Data is stored in issues.json and reporters.json.
Validation: Custom logic for IDs, email formats, and priority levels.

**API Endpoints**

Reporters
GET /api/reporters/ - Retrieve all reporters.
GET /api/reporters/<id>/ - Retrieve a specific reporter by ID.
POST /api/reporters/ - Create a new reporter.

Body: {"id": 1, "name": "John Doe", "email": "john@example.com", "team": "Backend"}

Issues
GET /api/issues/ - Retrieve all issues.
GET /api/issues/<id>/ - Retrieve a specific issue by ID.
POST /api/issues/ - Create a new issue.

Body: {"id": 101, "title": "Fix bug", "description": "...", "status": "open", "priority": "high", "reporter_id": 1}

Setup Instructions
Clone the repository:

git clone <repository-url>
cd devtrack
Set up Virtual Environment:

python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
Install Dependencies:

pip install django djangorestframework
Run the Server:

python manage.py runserver
Project Structure
issues/models.py: OOP classes and business logic.
issues/views.py: API endpoint implementations and JSON I/O.
issues/urls.py: Routing for the API.
data/: Directory containing issues.json and reporters.json.
