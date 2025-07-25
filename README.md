# User Management System API

A secure Flask-based REST API for user management with authentication, CRUD operations, and comprehensive security features.

## Features

- **User Management**: Create, read, update, delete users
- **Authentication**: Secure login with bcrypt password hashing
- **Search**: Find users by name with partial matching
- **Security**: SQL injection protection, input validation, password hashing
- **Thread Safety**: Thread-safe database operations
- **Comprehensive Testing**: Unit tests, security tests, and manual testing scripts

## Project Structure

```
├── app.py              # Main Flask application with API endpoints
├── models.py           # User model with database operations
├── database.py         # Database manager with connection handling
├── init_db.py          # Database initialization script
├── requirements.txt    # Python dependencies
├── users.db           # SQLite database file (created after init)
├── test_app.py        # Comprehensive unit tests
├── security_test.py   # Security vulnerability tests
├── manual_test.py     # Manual API testing script
├── quick_test.py      # Quick API connectivity test
├── start_test.py      # Application startup test
├── CHANGES.md         # Detailed changelog and refactoring notes
└── README.md          # This file
```

## File Descriptions

### Core Application Files

**`app.py`** - Main Flask application
- Defines all REST API endpoints
- Handles request validation and error responses
- Implements email validation and user data validation
- Provides endpoints for CRUD operations, authentication, and search

**`models.py`** - User data model
- User class with database operations (CRUD)
- Password hashing and verification using bcrypt
- Thread-safe database queries with parameterized statements
- Methods: `get_all()`, `get_by_id()`, `get_by_email()`, `save()`, `delete()`, `search_by_name()`

**`database.py`** - Database connection manager
- Thread-safe SQLite connection handling
- Context manager for automatic connection cleanup
- Prevents SQL injection with parameterized queries
- Singleton pattern for database manager

### Setup and Initialization

**`init_db.py`** - Database setup script
- Creates SQLite database with users table
- Initializes sample data with hashed passwords
- Sample users: john@example.com, jane@example.com, bob@example.com
- All sample passwords are properly hashed using bcrypt

**`requirements.txt`** - Python dependencies
- Flask 2.3.2 - Web framework
- Werkzeug 2.3.6 - WSGI utilities
- bcrypt 4.0.1 - Password hashing

### Testing Files

**`test_app.py`** - Comprehensive unit tests
- Tests all API endpoints with positive and negative scenarios
- Validates response formats and status codes
- Tests authentication, user creation, updates, and search
- Uses unittest framework with proper test isolation

**`security_test.py`** - Security testing script
- Tests SQL injection protection
- Validates password hashing implementation
- Checks input validation (email format, password length)
- Tests duplicate email prevention
- Verifies proper error handling

**`manual_test.py`** - Interactive testing script
- Manual verification of all API endpoints
- Provides detailed output for debugging
- Tests both success and failure scenarios
- Useful for development and troubleshooting

**`quick_test.py`** - Fast connectivity test
- Quick verification that API is running
- Tests basic endpoints with minimal output
- Useful for CI/CD or quick health checks

**`start_test.py`** - Application startup test
- Verifies the application can start properly
- Tests endpoints on a separate port to avoid conflicts
- Ensures all components are working together

### Documentation

**`CHANGES.md`** - Detailed refactoring documentation
- Lists all security improvements made
- Explains architectural decisions and trade-offs
- Documents what would be done with more time
- Provides context for code organization choices

## API Endpoints

### Health Check
- `GET /` - Returns API status and health information

### User Management
- `GET /users` - Get all users (passwords excluded)
- `GET /user/<id>` - Get specific user by ID
- `POST /users` - Create new user (requires name, email, password)
- `PUT /user/<id>` - Update user (name and/or email)
- `DELETE /user/<id>` - Delete user

### Authentication
- `POST /login` - Authenticate user (requires email, password)

### Search
- `GET /search?name=<query>` - Search users by name (partial matching)

## Installation and Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize database**:
   ```bash
   python init_db.py
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`

## Testing

### Run all unit tests:
```bash
python -m unittest test_app.py
```

### Run security tests:
```bash
python security_test.py
```

### Run manual tests:
```bash
python manual_test.py
```

### Quick connectivity test:
```bash
python quick_test.py
```

### Application startup test:
```bash
python start_test.py
```

## Sample Usage

### Create a user:
```bash
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com", "password": "securepass123"}'
```

### Login:
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com", "password": "securepass123"}'
```

### Get all users:
```bash
curl http://localhost:5000/users
```

### Search users:
```bash
curl "http://localhost:5000/search?name=John"
```

## Security Features

- **Password Hashing**: All passwords are hashed using bcrypt with salt
- **SQL Injection Protection**: Parameterized queries prevent SQL injection
- **Input Validation**: Email format validation and required field checking
- **Duplicate Prevention**: Email uniqueness enforced at database level
- **Thread Safety**: Thread-local database connections prevent race conditions
- **Error Handling**: Proper HTTP status codes and structured error responses

## Sample Login Credentials

After running `init_db.py`, you can use these credentials:
- **Email**: john@example.com, **Password**: password123
- **Email**: jane@example.com, **Password**: secret456
- **Email**: bob@example.com, **Password**: qwerty789

## Development Notes

This project was refactored from a basic implementation to include:
- Comprehensive security improvements
- Modular code organization
- Extensive testing suite
- Proper error handling
- Thread-safe database operations

See `CHANGES.md` for detailed information about the refactoring process and security improvements made.

## License

This project is for educational and demonstration purposes.