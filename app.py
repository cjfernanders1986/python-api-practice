from flask import Flask, request
import sqlite3
import requests
import os
from dotenv import load_dotenv
from github_service import count_languages, get_github_repositories

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)


# -----------------------------------
# HOME ROUTE
# -----------------------------------

@app.route("/")
def home():
    app_name = os.getenv("APP_NAME", "Customer API")
    return f"{app_name} is running!"


# -----------------------------------
# GET ALL CUSTOMERS
# -----------------------------------

@app.route("/customers", methods=["GET"])
def get_customers():
    connection = sqlite3.connect("business.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, email, city
        FROM customers
        ORDER BY name
    """)

    customers = cursor.fetchall()
    connection.close()

    customer_list = []

    for customer in customers:
        customer_list.append({
            "id": customer[0],
            "name": customer[1],
            "email": customer[2],
            "city": customer[3]
        })

    return customer_list


# -----------------------------------
# GET ONE CUSTOMER
# -----------------------------------

@app.route("/customers/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):
    connection = sqlite3.connect("business.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, email, city
        FROM customers
        WHERE id = ?
    """, (customer_id,))

    customer = cursor.fetchone()
    connection.close()

    if customer:
        return {
            "id": customer[0],
            "name": customer[1],
            "email": customer[2],
            "city": customer[3]
        }

    return {"message": "Customer not found"}, 404


# -----------------------------------
# ADD CUSTOMER
# -----------------------------------

@app.route("/customers", methods=["POST"])
def add_customer():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return {"message": "JSON data is required"}, 400

    name = data.get("name", "")
    email = data.get("email", "")
    city = data.get("city", "")

    if not all(isinstance(value, str) for value in (name, email, city)):
        return {"message": "Name, email, and city must be strings"}, 400

    name = name.strip()
    email = email.strip()
    city = city.strip()

    if not name:
        return {"message": "Name is required"}, 400

    if not email:
        return {"message": "Email is required"}, 400

    if not city:
        return {"message": "City is required"}, 400

    connection = sqlite3.connect("business.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO customers (name, email, city)
        VALUES (?, ?, ?)
    """, (name, email, city))

    connection.commit()
    connection.close()

    return {"message": "Customer added successfully"}, 201


# -----------------------------------
# UPDATE CUSTOMER
# -----------------------------------

@app.route("/customers/<int:customer_id>", methods=["PUT"])
def update_customer(customer_id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return {"message": "JSON data is required"}, 400

    name = data.get("name", "")
    email = data.get("email", "")
    city = data.get("city", "")

    if not all(isinstance(value, str) for value in (name, email, city)):
        return {"message": "Name, email, and city must be strings"}, 400

    name = name.strip()
    email = email.strip()
    city = city.strip()

    if not name:
        return {"message": "Name is required"}, 400

    if not email:
        return {"message": "Email is required"}, 400

    if not city:
        return {"message": "City is required"}, 400

    connection = sqlite3.connect("business.db")
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE customers
        SET name = ?, email = ?, city = ?
        WHERE id = ?
    """, (name, email, city, customer_id))

    connection.commit()
    updated = cursor.rowcount
    connection.close()

    if updated > 0:
        return {"message": "Customer updated successfully"}

    return {"message": "Customer not found"}, 404


# -----------------------------------
# DELETE CUSTOMER
# -----------------------------------

@app.route("/customers/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    connection = sqlite3.connect("business.db")
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM customers
        WHERE id = ?
    """, (customer_id,))

    connection.commit()
    deleted = cursor.rowcount
    connection.close()

    if deleted > 0:
        return {"message": "Customer deleted successfully"}

    return {"message": "Customer not found"}, 404


# -----------------------------------
# GITHUB REPOSITORY SUMMARY
# -----------------------------------

@app.route("/github/<username>", methods=["GET"])
def github_summary(username):
    language_filter = request.args.get("language")
    sort_by = request.args.get("sort")

    # Retrieve repositories from github_service.py
    try:
        repos = get_github_repositories(username)

    except requests.exceptions.Timeout:
        return {"message": "GitHub request timed out"}, 504

    except requests.exceptions.ConnectionError:
        return {"message": "Could not connect to GitHub"}, 503

    except requests.exceptions.RequestException:
        return {"message": "GitHub request failed"}, 502

    # Handle errors returned by github_service.py
    if isinstance(repos, tuple):
        return repos

    # Filter by programming language
    if language_filter:
        repos = [
            repo for repo in repos
            if (repo["language"] or "Unknown").lower()
            == language_filter.lower()
        ]

    # Sort alphabetically by repository name
    if sort_by == "name":
        repos = sorted(
            repos,
            key=lambda repo: repo["name"].lower()
        )

    # Sort by stars, highest first
    if sort_by == "stars":
        repos = sorted(
            repos,
            key=lambda repo: repo["stargazers_count"],
            reverse=True
        )

    # Count programming languages
    language_counts = count_languages(repos)

    # Return JSON summary
    return {
        "username": username,
        "total_repositories": len(repos),
        "languages": language_counts,
        "repositories": [
            {
                "name": repo["name"],
                "stars": repo["stargazers_count"]
            }
            for repo in repos
        ]
    }


# -----------------------------------
# START FLASK SERVER
# -----------------------------------

if __name__ == "__main__":
    app.run(debug=True)