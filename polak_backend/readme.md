# Polak - Reverse Polish Notation Calculator API

Polak is a FastAPI-based web service that computes mathematical expressions using Reverse Polish Notation (RPN) and stores calculation history in a database.

## Features

- Compute mathematical expressions in Reverse Polish Notation
- Store calculation history in a database
- Export calculation history as CSV
- Containerized with Docker for easy deployment

## What is Reverse Polish Notation?

Reverse Polish Notation (RPN), also known as postfix notation, is a mathematical notation where operators follow their operands. For example:

- Standard notation: `3 + 4`
- RPN: `3 4 +`

This eliminates the need for parentheses and makes calculations more straightforward for computers to process.

## Supported Operations

- Addition (`+`)
- Subtraction (`-`)
- Multiplication (`*`)
- Division (`/`)
- Exponentiation (`**`)

## API Endpoints

- `POST /compute-expression`: Compute a mathematical expression in RPN

  - Request body: `{"expression": "3 4 +"}`
  - Response: `{"result": 7.0}`

- `GET /operations`: Export all calculation history as CSV

## Getting Started

### Prerequisites

- Docker and Docker Compose

### Running the Application

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/polak.git
   cd polak
   ```

2. Start the application:

   ```bash
   docker-compose up -d
   ```

3. The API will be available at `http://localhost:8000`

### Example Usage

```bash
# Compute 3 + 4
curl -X POST http://localhost:8000/compute-expression \
  -H "Content-Type: application/json" \
  -d '{"expression": "3 4 +"}'

# Get calculation history as CSV
curl -X GET http://localhost:8000/operations -o operations.csv
```

## Development

### Project Structure

```
polak/
├── docker-compose.yml
├── polak_backend/
│   ├── polak/
│   │   ├── constants.py    # Configuration and constants
│   │   ├── core.py         # RPN calculation logic
│   │   ├── database.py     # Database connection and session management
│   │   ├── main.py         # FastAPI application and endpoints
│   │   ├── models.py       # SQLModel database models
│   │   └── tests.py        # Unit tests
```

### Running Tests

```bash
cd polak_backend
pytest
```

### Environment Variables

- `DB_URL`: Database connection string (default: `sqlite:///test_database.db`)
- `TEST_ENV`: Set to `True` for testing environment

## License

[MIT License](LICENSE)
