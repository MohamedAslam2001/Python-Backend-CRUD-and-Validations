Python Backend – CRUD & Validations (FastAPI)
📌 Project Overview

This project is a FastAPI-based backend application that provides JWT authentication and user-specific CRUD operations for managing products.
Each user can register, log in, and manage only their own data, with all authorization handled securely on the backend.

🔐 Authentication APIs
POST /register

Registers a new user

Validates unique email

Password is securely hashed before storing

POST /login

Authenticates user credentials

Returns a JWT access token

Token is used to access protected APIs

📦 Product APIs (JWT Protected)
POST /products

Creates a new product for the logged-in user

Product is linked to the user via JWT

GET /products

Returns only the products of the logged-in user

Prevents access to other users’ data

GET /products/{id}

Fetches a single product

Validates ownership before returning data

DELETE /products/{id}

Deletes a product

Ensures only the product owner can delete it

🛠 Requirements / Technologies Used

Python

FastAPI

Uvicorn

SQLAlchemy

MySQL

PyMySQL

JWT (python-jose)

bcrypt (passlib)

CORS Middleware
