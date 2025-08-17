#  ALX Travel App

A Django RESTful API for managing travel **Listings**, **Bookings**, and **Reviews**.

---

## Features

- CRUD operations via Django REST Framework
- Models:
  - `Listing`: Travel/accommodation offerings
  - `Booking`: Reservation of a listing
  - `Review`: User feedback and ratings
- API documentation with Swagger UI
- CORS enabled
- MySQL database support via `.env` config

---

## Project Setup

### 1. Clone and Install Dependencies

```bash
git clone https://github.com/yourusername/alx_travel_app.git
cd alx_travel_app
pip install -r requirements.txt



## API Endpoints for ALX Travel App


This document lists all available API endpoints for the **Listing**, **Booking**, and **Review** resources.

---

## 🔹 Listings

| Method | Endpoint           | Description                |
|--------|--------------------|----------------------------|
| GET    | /api/listings/     | List all listings          |
| POST   | /api/listings/     | Create a new listing       |
| GET    | /api/listings/{id}/| Retrieve a specific listing |
| PUT    | /api/listings/{id}/| Update a listing           |
| DELETE | /api/listings/{id}/| Delete a listing           |

---

## 🔹 Bookings

| Method | Endpoint            | Description                 |
|--------|---------------------|-----------------------------|
| GET    | /api/bookings/      | List all bookings           |
| POST   | /api/bookings/      | Create a new booking        |
| GET    | /api/bookings/{id}/ | Retrieve a specific booking |
| PUT    | /api/bookings/{id}/ | Update a booking            |
| DELETE | /api/bookings/{id}/ | Delete a booking            |

---

## 🔹 Reviews

| Method | Endpoint            | Description                 |
|--------|---------------------|-----------------------------|
| GET    | /api/reviews/       | List all reviews            |
| POST   | /api/reviews/       | Create a new review         |
| GET    | /api/reviews/{id}/  | Retrieve a specific review  |
| PUT    | /api/reviews/{id}/  | Update a review             |
| DELETE | /api/reviews/{id}/  | Delete a review             |

---

## 📚 API Documentation

- Swagger UI: `/swagger/`
- Redoc UI: `/redoc/`
- Raw Schema:
  - `/swagger.json`
  - `/swagger.yaml`