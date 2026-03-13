# API Versioning in FastAPI

## 1. What is API Versioning?

API Versioning is the practice of **managing multiple versions of an API** so that new changes do not break existing clients.

When an API evolves, endpoints may change:

- Request structure
- Response format
- Authentication methods
- Business logic

Versioning allows developers to **introduce improvements without breaking older applications**.

Example:

Old API
/api/users

Versioned API
/api/v1/users
/api/v2/users

---

# 2. Why API Versioning is Important

Without versioning:

Client applications may break when API changes.

Example problem:

Old response

{
"id":1,
"name":"Ashu"
}

New response

{
"id":1,
"first_name":"Ashu"
}

Old frontend will break.

Versioning solves this problem.

---

# 3. Common API Versioning Strategies

There are four major versioning strategies.

## 3.1 URI Versioning (Most Common)

Version number is added in the URL.

Example:

/api/v1/users
/api/v2/users

Advantages:

- Very simple
- Easy to test
- Easy for frontend developers

This is the **most commonly used method in FastAPI projects.**

---

## 3.2 Header Versioning

Version is passed in request headers.

Example:

Header

API-Version: v1

Endpoint

/api/users

---

## 3.3 Query Parameter Versioning

Version passed in query parameters.

Example

/api/users?version=1

---

## 3.4 Content Negotiation

Version is passed in Accept header.

Example

Accept: application/vnd.company.v1+json

---

# 4. Versioning Strategy Used in FastAPI

The most practical approach is:

URI Versioning

Example:

/api/v1/users
/api/v1/login

---