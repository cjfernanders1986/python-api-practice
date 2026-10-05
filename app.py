from flask import Flask, request
import sqlite3
import requests

app = Flask(__name__)


@app.route("/")
def home():
    return "Customer API is running!"


@app.route("/customers")
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

@app.route("/customers/<int:customer_id>")

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
    else:
        return {
            "message": "Customer not found"
        }, 404

@app.route("/customers", methods=["POST"])
def add_customer():
    data = request.get_json()

    # Validate the JSON data
    if not data:
        return {"message": "JSON data is required"}, 400

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    city = data.get("city", "").strip()

    if name == "":
        return {"message": "Name is required"}, 400

    if email == "":
        return {"message": "Email is required"}, 400

    if city == "":
        return {"message": "City is required"}, 400

    connection = sqlite3.connect("business.db")
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO customers (name, email, city)
    VALUES (?, ?, ?)
    """, (name, email, city))

    connection.commit()
    connection.close()

    return {
        "message": "Customer added successfully"
    }, 201
@app.route("/customers/<int:customer_id>", methods=["PUT"])
def update_customer(customer_id):
    data = request.get_json()

    # Validate the JSON data
    if not data:
        return {"message": "JSON data is required"}, 400

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    city = data.get("city", "").strip()

    if name == "":
        return {"message": "Name is required"}, 400

    if email == "":
        return {"message": "Email is required"}, 400

    if city == "":
        return {"message": "City is required"}, 400

    connection = sqlite3.connect("business.db")
    cursor = connection.cursor()

    cursor.execute("""
    UPDATE customers
    SET name = ?, email = ?, city = ?
    WHERE id = ?
    """, (name, email, city, customer_id))

    connection.commit()

    if cursor.rowcount > 0:
        connection.close()

        return {
            "message": "Customer updated successfully"
        }

    connection.close()

    return {
        "message": "Customer not found"
    }, 404
@app.route("/customers/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):

    connection = sqlite3.connect("business.db")
    cursor = connection.cursor()

    cursor.execute("""
    DELETE FROM customers
    WHERE id = ?
    """, (customer_id,))

    connection.commit()

    if cursor.rowcount > 0:
        connection.close()

        return {
            "message": "Customer deleted successfully"
        }

    connection.close()

    return {
        "message": "Customer not found"
    }, 404

def count_languages(repos):
    language_counts = {}

    for repo in repos:
        language = repo["language"] or "Unknown"

        if language in language_counts:
            language_counts[language] += 1
        else:
            language_counts[language] = 1

    return language_counts



def get_github_repositories(username):
    url = f"https://api.github.com/users/{username}/repos?per_page=100"

    response = requests.get(url, timeout=10)

    return response


def count_languages(repos):
    language_counts = {}

    for repo in repos:
        language = repo["language"] or "Unknown"

        if language in language_counts:
            language_counts[language] += 1
        else:
            language_counts[language] = 1

    return language_counts


@app.route("/github/<username>")
def github_summary(username):
    language_filter = request.args.get("language")
    sort_by = request.args.get("sort")

    try:
        response = get_github_repositories(username)

    except requests.exceptions.Timeout:
        return {
            "message": "GitHub request timed out"
        }, 504

    except requests.exceptions.ConnectionError:
        return {
            "message": "Could not connect to GitHub"
        }, 503

    if response.status_code == 404:
        return {
            "message": "GitHub user not found"
        }, 404

    if response.status_code != 200:
        return {
            "message": "GitHub API request failed",
            "status_code": response.status_code
        }, 502

    repos = response.json()
    if language_filter:
     repos = [
        repo for repo in repos
        if (repo["language"] or "Unknown").lower() == language_filter.lower()
    ]
     if sort_by == "name":
      repos = sorted(repos, key=lambda repo: repo["name"].lower())
      
      if sort_by == "stars":
       repos = sorted(
        repos,
        key=lambda repo: repo["stargazers_count"],
        reverse=True
    )


    language_counts = count_languages(repos)

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

if __name__ == "__main__":
    app.run(debug=True)