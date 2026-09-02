from flask import Flask, request
import sqlite3

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

if __name__ == "__main__":
    app.run(debug=True)