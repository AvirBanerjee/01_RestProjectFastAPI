
# FastAPI Authentication (JWT) – Complete Notes

## 1. Introduction to Authentication

Authentication is the process of **verifying the identity of a user** before allowing access to an application or API.

Example:

* User logs into an application using **email and password**
* Server verifies the credentials
* Server allows access if credentials are correct

Authentication is different from **Authorization**.

Authentication → *Who are you?*
Authorization → *What are you allowed to do?*

---

# 2. What is JWT (JSON Web Token)

JWT stands for **JSON Web Token**.

It is a **secure way to transmit information between client and server** using a digitally signed token.

JWT is widely used for **API authentication** in modern applications like:

* FastAPI
* Node.js
* Django
* React apps
* Mobile apps

Instead of storing sessions on the server, JWT allows **stateless authentication**.

---

# 3. Structure of JWT

A JWT token contains **three parts**:

```
HEADER.PAYLOAD.SIGNATURE
```

Example:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
.
eyJzdWIiOiJhc2h1QGdtYWlsLmNvbSIsImV4cCI6MTY5NzQ2NTYwMH0
.
SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

### 1. Header

Contains information about algorithm.

Example:

```json
{
 "alg": "HS256",
 "typ": "JWT"
}
```

---

### 2. Payload

Contains user data.

Example:

```json
{
 "sub": "ashu@gmail.com",
 "exp": 1710000000
}
```

Common payload fields:

| Field | Meaning                   |
| ----- | ------------------------- |
| sub   | subject (user identifier) |
| exp   | expiration time           |
| iat   | issued at                 |
| iss   | issuer                    |

---

### 3. Signature

Used to verify token integrity.

Signature ensures that **token is not modified**.

---

# 4. Authentication Flow in FastAPI

Typical JWT authentication flow:

### Step 1: User Registers

```
POST /users
```

User sends:

```
name
email
password
```

Password is **hashed before storing in database**.

---

### Step 2: User Login

```
POST /login
```

User sends:

```
username
password
```

Server:

1. verifies credentials
2. generates JWT token
3. returns token

Example response:

```json
{
 "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
 "token_type": "bearer"
}
```

---

### Step 3: Client Stores Token

Client stores token in:

* localStorage
* cookies
* memory

---

### Step 4: Client Sends Token

When calling protected APIs:

```
Authorization: Bearer TOKEN
```

Example request header:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

### Step 5: Server Validates Token

Server:

1. decodes JWT
2. checks signature
3. checks expiration
4. fetches user

If valid → access granted.

---

# 5. Required Libraries for FastAPI Authentication

Install these libraries:

```
pip install python-jose passlib[bcrypt] python-multipart
```

### Library Explanation

| Library          | Purpose                  |
| ---------------- | ------------------------ |
| python-jose      | create and verify JWT    |
| passlib          | password hashing         |
| bcrypt           | secure hashing algorithm |
| python-multipart | form data support        |

---

# 6. Password Hashing

Passwords should **never be stored in plain text**.

Instead we use **bcrypt hashing**.

Example:

```
password = "123456"
```

Hashed version:

```
$2b$12$P8vT9hE3s3WZC....
```

### Hashing Function

```python
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)
```

---

### Password Verification

```python
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
```

---

# 7. OAuth2 Password Flow

FastAPI uses **OAuth2PasswordBearer**.

It extracts token from:

```
Authorization: Bearer TOKEN
```

Example:

```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
```

This tells FastAPI that **/login endpoint returns tokens**.

---

# 8. Creating JWT Token

Token creation function:

```python
def create_access_token(data:dict):

    to_encode=data.copy()

    expire=datetime.utcnow()+timedelta(minutes=30)

    to_encode.update({"exp":expire})

    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt
```

Payload typically contains:

```
sub = user email or user id
```

---

# 9. Getting Current User

Protected APIs must verify token.

Example:

```python
def get_current_user(token:str=Depends(oauth2_scheme)):

    payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])

    email=payload.get("sub")

    user=db.query(UserDB).filter(UserDB.email==email).first()

    return user
```

---

# 10. Protecting Routes

Example:

```
GET /users
```

Protected version:

```python
@app.get("/users")
def get_users(current_user:UserDB = Depends(get_current_user)):
```

Now token is required.

---

# 11. API Authentication Example

### Register

```
POST /users
```

Body:

```json
{
"name":"Ashutosh",
"email":"ashu@gmail.com",
"password":"123456"
}
```

---

### Login

```
POST /login
```

Form data:

```
username = ashu@gmail.com
password = 123456
```

---

### Access Protected API

```
GET /users
```

Header:

```
Authorization: Bearer TOKEN
```

---

# 12. Advantages of JWT

1. Stateless authentication
2. No server session storage
3. Works well with microservices
4. Fast and scalable
5. Works across web and mobile

---

# 13. Disadvantages of JWT

1. Token cannot be revoked easily
2. Larger payload size
3. Security risk if token leaked

---

# 14. Best Practices

Use these in production:

* Always hash passwords
* Use HTTPS
* Use strong secret keys
* Use short token expiration
* Implement refresh tokens
* Use role-based access control

---

# 15. Advanced Authentication Concepts

### Refresh Tokens

Used to generate new access tokens.

Example flow:

```
access token → expires
refresh token → generate new token
```

---

### Role Based Authorization

Example roles:

```
admin
user
manager
```

Example:

```
only admin can delete users
```

---

### Email Verification

User must verify email before login.

---

### Password Reset

User can reset password using email link.

---

# 16. Production Architecture

Large FastAPI projects use this structure:

```
app
 ├── main.py
 ├── database.py
 ├── models
 ├── schemas
 ├── routers
 ├── services
 ├── auth
 └── utils
```

Authentication usually lives in:

```
auth/
 ├── jwt_handler.py
 ├── password.py
 └── dependencies.py
```

---

# 17. Summary

Authentication system includes:

1. User registration
2. Password hashing
3. Login endpoint
4. JWT token generation
5. Token validation
6. Protected routes

JWT allows **secure stateless authentication** for modern APIs.

---

# End of Notes
