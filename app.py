"""
app.py — FastAPI REST API for the Movie Ticket Booking System (MongoDB)

Run: python3 -m uvicorn app:app --reload
Then test endpoints:
  - Using Postman at http://localhost:8000
  - Or using the built-in Swagger docs at http://localhost:8000/docs

Requires: pip3 install fastapi uvicorn pymongo pydantic
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime
from connection import get_db

app = FastAPI(title="Movie Ticket Booking System API")
db = get_db()


# Helper functions

def serialize(doc):
    """Convert MongoDB's ObjectId/datetime into JSON-friendly strings."""
    if doc is None:
        return None
    doc["_id"] = str(doc["_id"])
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            doc[key] = str(value)
        if isinstance(value, datetime):
            doc[key] = value.isoformat()
        if isinstance(value, list):
            doc[key] = [str(v) if isinstance(v, ObjectId) else v for v in value]
    return doc


def to_object_id(id_str):
    try:
        return ObjectId(id_str)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid ID format")



# Pydantic models — define what a valid request body looks like
# (FastAPI uses these to auto-validate incoming JSON)

class Address(BaseModel):
    label: str = "Home"
    city: str
    pincode: str


class UserCreate(BaseModel):
    name: str
    email: str
    phone: str
    addresses: List[Address] = []


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class MovieCreate(BaseModel):
    title: str
    genre: List[str] = []
    cast: List[str] = []
    duration_min: int
    release_date: str   # format: "YYYY-MM-DD"
    language: str = ""


class Screen(BaseModel):
    screen_no: int
    capacity: int
    type: str


class TheaterCreate(BaseModel):
    name: str
    city: str
    screens: List[Screen] = []


class Seat(BaseModel):
    seat_no: str
    status: str = "available"


class ShowCreate(BaseModel):
    movie_id: str
    theater_id: str
    screen_no: int = 1
    start_time: str   # format: "YYYY-MM-DDTHH:MM:SS"
    price: float
    seat_map: List[Seat] = []


class Payment(BaseModel):
    status: str = "pending"
    method: Optional[str] = None
    txn_id: Optional[str] = None


class BookingCreate(BaseModel):
    user_id: str
    show_id: str
    seats_booked: List[str]
    total_amount: float
    payment: Payment = Payment()


class PaymentStatusUpdate(BaseModel):
    status: str


class ReviewCreate(BaseModel):
    movie_id: str
    user_id: str
    rating: int
    comment: str = ""


class ReviewUpdate(BaseModel):
    rating: Optional[int] = None
    comment: Optional[str] = None


class AISummaryCreate(BaseModel):
    movie_id: str
    summary_text: str
    sentiment: str = ""
    based_on_review_ids: List[str] = []
    model_used: str = "claude-sonnet-5"



# USERS

@app.post("/users", status_code=201)
def create_user(user: UserCreate):
    result = db.users.insert_one({
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "addresses": [a.dict() for a in user.addresses],
        "created_at": datetime.utcnow()
    })
    return {"inserted_id": str(result.inserted_id)}


@app.get("/users")
def get_users():
    return [serialize(u) for u in db.users.find()]


@app.get("/users/{user_id}")
def get_user(user_id: str):
    oid = to_object_id(user_id)
    user = db.users.find_one({"_id": oid})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return serialize(user)


@app.put("/users/{user_id}")
def update_user(user_id: str, user: UserUpdate):
    oid = to_object_id(user_id)
    updates = {k: v for k, v in user.dict().items() if v is not None}
    result = db.users.update_one({"_id": oid}, {"$set": updates})
    return {"matched": result.matched_count, "modified": result.modified_count}


@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    oid = to_object_id(user_id)
    result = db.users.delete_one({"_id": oid})
    return {"deleted": result.deleted_count}


# MOVIES

@app.post("/movies", status_code=201)
def create_movie(movie: MovieCreate):
    result = db.movies.insert_one({
        "title": movie.title,
        "genre": movie.genre,
        "cast": movie.cast,
        "duration_min": movie.duration_min,
        "release_date": datetime.strptime(movie.release_date, "%Y-%m-%d"),
        "language": movie.language
    })
    return {"inserted_id": str(result.inserted_id)}


@app.get("/movies")
def get_movies():
    return [serialize(m) for m in db.movies.find()]


# THEATERS

@app.post("/theaters", status_code=201)
def create_theater(theater: TheaterCreate):
    result = db.theaters.insert_one({
        "name": theater.name,
        "city": theater.city,
        "screens": [s.dict() for s in theater.screens]
    })
    return {"inserted_id": str(result.inserted_id)}


@app.get("/theaters")
def get_theaters():
    return [serialize(t) for t in db.theaters.find()]

# SHOWS

@app.post("/shows", status_code=201)
def create_show(show: ShowCreate):
    result = db.shows.insert_one({
        "movie_id": to_object_id(show.movie_id),
        "theater_id": to_object_id(show.theater_id),
        "screen_no": show.screen_no,
        "start_time": datetime.strptime(show.start_time, "%Y-%m-%dT%H:%M:%S"),
        "price": show.price,
        "seat_map": [s.dict() for s in show.seat_map]
    })
    return {"inserted_id": str(result.inserted_id)}


@app.get("/shows")
def get_shows():
    return [serialize(s) for s in db.shows.find()]


@app.get("/shows/{show_id}/available-seats")
def available_seats(show_id: str):
    oid = to_object_id(show_id)
    show = db.shows.find_one({"_id": oid})
    if not show:
        raise HTTPException(status_code=404, detail="Show not found")
    return [s for s in show.get("seat_map", []) if s["status"] == "available"]


# BOOKINGS

@app.post("/bookings", status_code=201)
def create_booking(booking: BookingCreate):
    show_oid = to_object_id(booking.show_id)
    result = db.bookings.insert_one({
        "user_id": to_object_id(booking.user_id),
        "show_id": show_oid,
        "seats_booked": booking.seats_booked,
        "total_amount": booking.total_amount,
        "payment": booking.payment.dict(),
        "booked_at": datetime.utcnow()
    })
    # mark those seats as booked
    for seat_no in booking.seats_booked:
        db.shows.update_one(
            {"_id": show_oid, "seat_map.seat_no": seat_no},
            {"$set": {"seat_map.$.status": "booked"}}
        )
    return {"inserted_id": str(result.inserted_id)}


@app.get("/bookings")
def get_bookings():
    return [serialize(b) for b in db.bookings.find()]


@app.get("/bookings/with-user")
def bookings_with_user():
    """JOIN-like read using $lookup."""
    pipeline = [
        {"$lookup": {"from": "users", "localField": "user_id",
                      "foreignField": "_id", "as": "user_info"}}
    ]
    results = [serialize(doc) for doc in db.bookings.aggregate(pipeline)]
    for r in results:
        r["user_info"] = [serialize(u) for u in r.get("user_info", [])]
    return results


@app.put("/bookings/{booking_id}/payment-status")
def update_payment_status(booking_id: str, payload: PaymentStatusUpdate):
    oid = to_object_id(booking_id)
    result = db.bookings.update_one(
        {"_id": oid},
        {"$set": {"payment.status": payload.status}}
    )
    return {"modified": result.modified_count}


@app.delete("/bookings/{booking_id}")
def delete_booking(booking_id: str):
    oid = to_object_id(booking_id)
    result = db.bookings.delete_one({"_id": oid})
    return {"deleted": result.deleted_count}


# REVIEWS

@app.post("/reviews", status_code=201)
def create_review(review: ReviewCreate):
    result = db.reviews.insert_one({
        "movie_id": to_object_id(review.movie_id),
        "user_id": to_object_id(review.user_id),
        "rating": review.rating,
        "comment": review.comment,
        "created_at": datetime.utcnow()
    })
    return {"inserted_id": str(result.inserted_id)}


@app.get("/reviews/with-user")
def reviews_with_user():
    pipeline = [
        {"$lookup": {"from": "users", "localField": "user_id",
                      "foreignField": "_id", "as": "user_info"}}
    ]
    results = [serialize(doc) for doc in db.reviews.aggregate(pipeline)]
    for r in results:
        r["user_info"] = [serialize(u) for u in r.get("user_info", [])]
    return results


@app.put("/reviews/{review_id}")
def update_review(review_id: str, review: ReviewUpdate):
    oid = to_object_id(review_id)
    updates = {k: v for k, v in review.dict().items() if v is not None}
    result = db.reviews.update_one({"_id": oid}, {"$set": updates})
    return {"modified": result.modified_count}


@app.delete("/reviews/{review_id}")
def delete_review(review_id: str):
    oid = to_object_id(review_id)
    result = db.reviews.delete_one({"_id": oid})
    return {"deleted": result.deleted_count}


# AI SUMMARIES

@app.post("/ai-summaries", status_code=201)
def create_ai_summary(summary: AISummaryCreate):
    result = db.ai_summaries.insert_one({
        "movie_id": to_object_id(summary.movie_id),
        "summary_text": summary.summary_text,
        "sentiment": summary.sentiment,
        "based_on_review_ids": [to_object_id(r) for r in summary.based_on_review_ids],
        "model_used": summary.model_used,
        "generated_at": datetime.utcnow()
    })
    return {"inserted_id": str(result.inserted_id)}


@app.get("/ai-summaries")
def get_ai_summaries():
    return [serialize(s) for s in db.ai_summaries.find()]
