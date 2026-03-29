from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt_identity
)
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Config
app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY")

# Init
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# MongoDB
client = MongoClient(os.getenv("MONGO_URI"))
db = client["auth_db"]
users_collection = db["users"]

# ------------------------
# Register
# ------------------------
@app.route("/register", methods=["POST"])
def register():
    data = request.json

    if users_collection.find_one({"email": data["email"]}):
        return jsonify({"error": "Email already exists"}), 400

    hashed_pw = bcrypt.generate_password_hash(data["password"]).decode("utf-8")

    users_collection.insert_one({
        "username": data["username"],
        "email": data["email"],
        "password": hashed_pw
    })

    return jsonify({"message": "User registered successfully"}), 201

# ------------------------
# Login (returns JWT)
# ------------------------
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = users_collection.find_one({"email": data["email"]})

    if not user or not bcrypt.check_password_hash(user["password"], data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=str(user["_id"]))

    return jsonify({
        "access_token": access_token
    })

# ------------------------
# Protected Route
# ------------------------
@app.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    user_id = get_jwt_identity()

    return jsonify({
        "message": "Access granted",
        "user_id": user_id
    })

# ------------------------
# Run
# ------------------------
if __name__ == "__main__":
    app.run(debug=True)
