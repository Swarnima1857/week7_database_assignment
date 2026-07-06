"""
connection.py — MongoDB connection handler
"""

from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "movie_booking"


def get_db():
    """Returns the database handle. Call this from any other module."""
    client = MongoClient(MONGO_URI)
    return client[DB_NAME]