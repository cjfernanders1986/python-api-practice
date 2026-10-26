# Python API Practice

A Python learning project that demonstrates database management, REST API development, and integration with external APIs.

This project started as a way to refresh my Python programming skills and gradually expanded into a Customer Management System and a Flask REST API.

## Project Features

- Customer Management System using Python and SQLite
- Command-line interface for managing customers
- Flask REST API with full CRUD operations
- Integration with the GitHub REST API
- GitHub repository filtering and sorting
- GitHub API pagination
- Repository statistics by programming language
- Environment variable configuration using `.env`
- HTTP error handling and input validation
- Modular Python code organization

## Technologies Used

- Python 3
- Flask
- SQLite
- SQL
- Requests
- REST APIs
- JSON
- python-dotenv
- Git
- GitHub
- Visual Studio Code

## Customer Management System

A command-line application that stores customer information in a SQLite database.

### Features

- Add new customers
- Search customers by name
- View all customers
- Update customer information by ID
- Delete customers by ID
- Confirm before deleting a customer
- Validate user input
- Store customer records using SQLite

### What I Learned

While building the Customer Management System, I practiced:

- Connecting Python to SQLite databases
- Creating database tables
- Using SQL `INSERT`, `SELECT`, `UPDATE`, and `DELETE`
- Writing parameterized SQL queries
- Working with Python loops and conditional statements
- Validating user input
- Managing records using unique IDs
- Building command-line menus

### Run the Customer Management System

```bash
python database.py
```

## Flask REST API

The project includes a Flask REST API connected to the SQLite customer database.

### Customer API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Check that the application is running |
| GET | `/customers` | Retrieve all customers |
| GET | `/customers/<id>` | Retrieve one customer by ID |
| POST | `/customers` | Add a new customer |
| PUT | `/customers/<id>` | Update an existing customer |
| DELETE | `/customers/<id>` | Delete a customer |

### API Features

- JSON request and response data
- SQLite database integration
- Full CRUD operations
- Input validation
- HTTP 400 responses for invalid requests
- HTTP 404 responses for missing customers

### Example: Retrieve All Customers

**Request:**

```http
GET /customers
```

**Example response:**

```json
[
  {
    "id": 4,
    "name": "Alice Brown",
    "email": "alice@example.com",
    "city": "Hoboken"
  },
  {
    "id": 5,
    "name": "Bob Wilson",
    "email": "bob@example.com",
    "city": "Jersey City"
  }
]
```

### Example: Retrieve One Customer

**Request:**

```http
GET /customers/4
```

**Example response:**

```json
{
  "id": 4,
  "name": "Alice Brown",
  "email": "alice@example.com",
  "city": "Hoboken"
}
```

### Example: Customer Not Found

**Request:**

```http
GET /customers/9999
```

**Response:**

```json
{
  "message": "Customer not found"
}
```

HTTP status: `404 Not Found`

## GitHub REST API Integration

The Flask application connects to the public GitHub REST API to retrieve and analyze repositories belonging to a GitHub user.

### GitHub API Endpoint

```http
GET /github/<username>
```

Example:

```text
http://127.0.0.1:5000/github/cjfernanders1986
```

### GitHub API Features

- Retrieve a GitHub user's public repositories
- Retrieve multiple pages of repository results
- Filter repositories by programming language
- Sort repositories alphabetically by name
- Sort repositories by number of stars
- Count repositories by programming language
- Return repository names and star counts
- Handle invalid GitHub usernames
- Handle connection errors and timeouts
- Support an optional GitHub API token

### Filter Repositories by Language

Use the `language` query parameter:

```text
http://127.0.0.1:5000/github/cjfernanders1986?language=Python
```

This returns only repositories whose primary language is Python.

Language filtering is case-insensitive.

### Sort Repositories by Name

Use the `sort=name` query parameter:

```text
http://127.0.0.1:5000/github/cjfernanders1986?sort=name
```

This returns repositories in alphabetical order.

### Sort Repositories by Stars

Use the `sort=stars` query parameter:

```text
http://127.0.0.1:5000/github/cjfernanders1986?sort=stars
```

This returns repositories with the most stars first.

### Combine Filtering and Sorting

You can combine query parameters:

```text
http://127.0.0.1:5000/github/cjfernanders1986?language=Python&sort=name
```

This returns Python repositories sorted alphabetically.

### Example GitHub API Response

```json
{
  "username": "exampleuser",
  "total_repositories": 2,
  "languages": {
    "Python": 2
  },
  "repositories": [
    {
      "name": "project-one",
      "stars": 5
    },
    {
      "name": "project-two",
      "stars": 2
    }
  ]
}
```

The repository names and counts above are illustrative examples.

### GitHub API Error Handling

If a GitHub username does not exist, the API returns:

```json
{
  "error": "GitHub user not found"
}
```

HTTP status: `404 Not Found`

The API also handles GitHub request failures, connection errors, and timeouts.

## External API Practice Scripts

This repository includes additional Python scripts for practicing external REST API requests.

Examples include:

- `external_api.py` — basic external API requests
- `country_lookup.py` — REST Countries API practice
- `github_lookup.py` — GitHub user lookup
- `github_repos.py` — GitHub repository analysis

These scripts demonstrate how to:

- Send HTTP GET requests
- Read JSON responses
- Work with nested JSON data
- Check HTTP status codes
- Process API responses
- Handle request errors

## Project Structure

```text
python-api-practice/
│
├── app.py
├── github_service.py
├── database.py
├── external_api.py
├── country_lookup.py
├── github_lookup.py
├── github_repos.py
├── env_test.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env
└── business.db
```

**Note:** The `.env` file and `business.db` database are local files excluded from Git tracking. They are not included when cloning the repository.

### Code Organization

- `app.py` contains the Flask routes and customer API operations.
- `github_service.py` contains GitHub API requests, pagination, and language-counting functions.
- `database.py` contains the command-line Customer Management System.

Separating code into modules makes the project easier to understand and maintain.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/cjfernanders1986/python-api-practice.git
```

Navigate into the project folder:

```bash
cd python-api-practice
```

### 2. Create a Virtual Environment

On Windows:

```powershell
python -m venv .venv
```

Activate it in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs the required Python packages, including Flask, Requests, and python-dotenv.

### 4. Configure Environment Variables

Create a file named `.env` in the project folder.

Add:

```env
APP_NAME=My Python Flask API
GITHUB_TOKEN=
```

The GitHub token is optional for public repository requests.

If you use a token, keep it private and never commit it to GitHub.

### 5. Set Up the Customer Database

The project uses a local SQLite database named `business.db`.

Because the database is excluded from Git, you must create it locally.

Run the Customer Management System:

```bash
python database.py
```

The program automatically creates the `business.db` file and the `customers` table if they do not already exist.

You can use the menu to add customer records.

Choose option `6` to exit the program.

After initializing the database, you can start the Flask API using:

```bash
python app.py
```

### 6. Start the Flask Server

```bash
python app.py
```

The development server runs locally at:

```text
http://127.0.0.1:5000
```

Open this address in your browser to verify that the API is running.

### 7. Test the API

Customer endpoints:

```text
http://127.0.0.1:5000/customers
```

```text
http://127.0.0.1:5000/customers/4
```

GitHub endpoints:

```text
http://127.0.0.1:5000/github/cjfernanders1986
```

```text
http://127.0.0.1:5000/github/cjfernanders1986?language=Python
```

```text
http://127.0.0.1:5000/github/cjfernanders1986?sort=stars
```

The customer IDs shown are examples and depend on the records in your local database.

## Environment Variables and Security

This project uses `python-dotenv` to load configuration values from a local `.env` file.

The `.gitignore` file excludes:

```gitignore
.venv/
business.db
.env
__pycache__/
```

This prevents local environments, database files, environment variables, and Python cache files from being accidentally committed.

## What I Learned

Through this project, I practiced:

- Python functions, loops, and conditionals
- SQLite database operations
- SQL queries and parameterized statements
- Flask application development
- REST API design
- CRUD operations
- HTTP methods and status codes
- JSON request and response handling
- Consuming external REST APIs
- API query parameters
- Filtering and sorting data
- API pagination
- Handling errors and exceptions
- Environment variables
- Organizing Python code into modules
- Managing dependencies
- Git version control
- Pushing projects to GitHub

## Future Improvements

Possible next steps include:

- Automated API tests using pytest
- Improved database initialization and migrations
- Pagination for customer records
- Additional customer search and filtering
- API authentication
- Deployment to a cloud hosting platform

## Author

Created by [cjfernanders1986](https://github.com/cjfernanders1986) as part of a hands-on Python learning journey.