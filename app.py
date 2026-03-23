from flask import Flask, request, jsonify, session
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from bson.objectid import ObjectId
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# MongoDB Atlas connection
client = MongoClient(os.getenv("MONGO_URI"))
db = client["auth_db"]
users_collection = db["users"]

bcrypt = Bcrypt(app)

# ------------------------
# Register
# ------------------------
@app.route("/register", methods=["POST"])
def register():
    from flask_bcrypt import Bcrypt
    bcrypt = Bcrypt()    

    password = "123456"
    hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")
    print(hashed_pw)
    print("Stored hash:", user["password"])
    print("Input password:", data["password"])
    print("Check:", bcrypt.check_password_hash(user["password"], data["password"]))


# ------------------------
# Login
# ------------------------
@app.route("/login", methods=["POST"])
def login():


    data = request.json

    user = users_collection.find_one({"email": data["email"]})

    if not user or not bcrypt.check_password_hash(user["password"], data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    session["user_id"] = str(user["_id"])

    return jsonify({
        "message": "Login successful",
        "user": {
            "id": str(user["_id"]),
            "username": user["username"],
            "email": user["email"]
        }
    })

# ------------------------
# Profile (protected)
# ------------------------
@app.route("/profile", methods=["GET"])
def profile():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user = users_collection.find_one({"_id": ObjectId(session["user_id"])})

    return jsonify({
        "username": user["username"],
        "email": user["email"]
    })

# ------------------------
# Logout
# ------------------------
@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)
    return jsonify({"message": "Logged out"})

if __name__ == "__main__":
    app.run(debug=True)
