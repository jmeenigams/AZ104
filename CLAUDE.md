# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This repo contains a Flask REST API with JWT-based authentication backed by MongoDB Atlas, along with an Ansible quickstart configuration.

## Running the App

```bash
# Activate the virtual environment
source venv/Scripts/activate  # or venv\Scripts\activate.bat on Windows cmd

# Run the Flask app
python app.py
```

The app runs on `http://127.0.0.1:5000` in debug mode.

## Environment Setup

Copy `.env` and populate:
- `MONGO_URI` — MongoDB Atlas connection string
- `SECRET_KEY` — JWT signing secret

Dependencies are installed in `venv/`. To reinstall (no requirements.txt exists — derive from imports):
- `flask`, `flask-bcrypt`, `flask-jwt-extended`, `pymongo`, `python-dotenv`

## API Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/register` | None | Create user (`username`, `email`, `password`) |
| POST | `/login` | None | Returns JWT `access_token` |
| GET | `/profile` | Bearer JWT | Returns authenticated user ID |

## Architecture

**`app.py`** — single-file Flask app:
- MongoDB Atlas (`auth_db.users` collection) stores users with bcrypt-hashed passwords
- `flask-jwt-extended` issues and validates JWTs; identity is the MongoDB `_id` as a string
- No blueprint/factory pattern — all routes are defined at module level

**`ansible_quickstart/inventory.ini`** — placeholder Ansible inventory with three hosts (`192.0.2.50–52`), no playbooks present yet.
