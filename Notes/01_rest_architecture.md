# What is REST?

REST = **Representational State Transfer**

REST is an architectural style for designing web APIs using HTTP.

It is:

- ❌ Not a protocol  
- ❌ Not a library  
- ✅ A set of design principles  

When we build APIs in **Django REST Framework**, **Flask**, or **FastAPI**, we usually follow REST principles.

---

# 2️⃣ Why REST Exists?

Imagine this:

Frontend (React / Mobile App) needs data  
Backend (Django / Flask / FastAPI) provides data  

They must communicate in a structured and standardized way.

REST defines:

- How URLs should look  
- Which HTTP methods to use  
- How responses should be formatted  
- How errors should be handled  

Without REST → APIs become inconsistent and messy.

---

# 3️⃣ REST Architecture – Visual Understanding

### Flow:

Client → HTTP Request → Server → Database  
Server → HTTP Response → Client  

```
Client  →  HTTP Request  →  Server  →  Database
Client  ←  HTTP Response ←  Server
```

---

# 4️⃣ Core REST Constraints (Very Important)

REST has **6 constraints**.

---

## 1️⃣ Client–Server Separation

Frontend and backend are separate systems.

Example:

- React app = Client  
- Django API = Server  

### Benefits:

- Independent development  
- Scalability  
- Separation of concerns  

---

## 2️⃣ Stateless

Server does NOT store client state.

Every request must contain all necessary information.

### Example:

JWT token sent in every request

No session dependency.

### ❌ Wrong:
Server remembers previous request.

### ✅ Correct:
Every request is independent.

---

## 3️⃣ Cacheable

Response must define whether it can be cached.

Example:

```
Cache-Control: max-age=3600
```

This improves performance and reduces server load.

---

## 4️⃣ Uniform Interface (MOST IMPORTANT)

Rules:

- Resource-based URLs  
- Proper HTTP methods  
- Standard status codes  
- JSON format  

This makes APIs predictable and standardized.

---

## 5️⃣ Layered System

Client does not know if:

- It is talking directly to the server  
- Through a load balancer  
- Through an API gateway  
- Through a reverse proxy  

This allows scalable architecture.

---

## 6️⃣ Code on Demand (Optional)

Server can send executable code.

Rarely used in modern REST APIs.

---

# 5️⃣ What is a Resource?

In REST:

Everything is a **resource**.

Examples:

- User  
- Product  
- Order  
- Blog  

Each resource has:

- Unique URI  
- Representation (usually JSON)  

### Example:

```
/users
/products
/orders
```

---

# 6️⃣ REST Patterns (Core Section)

Now we go deeper.

---

## Pattern 1 – Resource-Based Routing

### ❌ BAD Design:

```
/getUsers
/createUser
/deleteUser
```

### ✅ GOOD Design:

```
GET     /users
POST    /users
GET     /users/1
PUT     /users/1
DELETE  /users/1
```

This follows REST principles.

---

## Pattern 2 – Proper HTTP Methods

| Method  | Meaning            | Example |
|----------|------------------|----------|
| GET      | Read              | Get users |
| POST     | Create            | Add user |
| PUT      | Replace           | Update full user |
| PATCH    | Partial update    | Update email only |
| DELETE   | Remove            | Delete user |

---

### Example (Flask)

```python
@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users)

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    return jsonify(data), 201
```

---

## Pattern 3 – Use Proper Status Codes

| Code | Meaning |
|------|----------|
| 200  | OK |
| 201  | Created |
| 400  | Bad Request |
| 401  | Unauthorized |
| 403  | Forbidden |
| 404  | Not Found |
| 500  | Server Error |

### Example:

```python
return jsonify({"error": "User not found"}), 404
```

---

## Pattern 4 – Stateless Authentication

Use:

- JWT
- Token-based authentication

Do NOT use:

- Server memory sessions (in pure REST APIs)

Each request must carry authentication credentials.

---

# ✅ Final REST Summary

REST is about:

- Clean URLs  
- Proper HTTP methods  
- Stateless design  
- Standard status codes  
- JSON communication  
- Resource-based architecture  

It creates scalable, maintainable, and predictable APIs.

---

# 🚀 For Teaching Use

You can use this document to explain:

- REST basics
- Architecture constraints
- Resource design
- HTTP standards
- API best practices

---
