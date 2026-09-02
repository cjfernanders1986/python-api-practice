# Python API Practice

My first Python project while refreshing my programming skills.

## What it does

- Connects to a public REST API
- Retrieves JSON data
- Processes user information
- Searches users based on location
- Displays user information

## Technologies

- Python
- Requests
- REST API
- JSON
- Git
- GitHub

# Customer Management System

A command-line Customer Management System built with Python and SQLite.

The application allows users to add, search, view, update, and delete customer records stored in a SQLite database.

## Features

- Add new customers
- Search customers by name
- View all customers
- Update customer information by ID
- Delete customers by ID
- Confirm before deleting a customer
- Validate user input
- Store customer data using SQLite

## Technologies Used

- Python
- SQLite
- SQL

## What I Learned

While building the Customer Management System, I practiced:

- Connecting Python to a SQLite database
- Creating database tables
- Using SQL `INSERT`, `SELECT`, `UPDATE`, and `DELETE`
- Writing parameterized SQL queries
- Using Python loops and conditional statements
- Validating user input
- Handling database records by unique ID
- Building a command-line menu

## How to Run

1. Clone the repository.
2. Open the project folder in VS Code.
3. Make sure Python is installed.
4. Run the program:

## REST API

This project also includes a Flask REST API connected to the SQLite customer database.

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /customers | Get all customers |
| GET | /customers/<id> | Get one customer |
| POST | /customers | Add a new customer |
| PUT | /customers/<id> | Update a customer |
| DELETE | /customers/<id> | Delete a customer |

### API Features

- JSON request and response data
- SQLite database integration
- Full CRUD operations
- Input validation
- 400 Bad Request responses for invalid data
- 404 Not Found responses for missing customers

### Run the API

Install Flask:

```bash
pip install flask

The API runs locally at:

http://127.0.0.1:5000
