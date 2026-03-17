"""
MongoDB Connection Manager for Honeypot
========================================
Central database module — all other modules import `get_db()` from here.

Collections:
  - commands        : One document per command executed by attacker
  - sessions        : One document per SSH session (metadata + analysis)
  - session_replays : Full transcript per session (for replay feature)

Connection:
  Default: mongodb://localhost:27017
  Override via MONGO_URI environment variable.
"""

import os
from pymongo import MongoClient, ASCENDING, DESCENDING

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.environ.get("MONGO_DB_NAME", "honeypot_db")

# ---------------------------------------------------------------------------
# SINGLETON CONNECTION
# ---------------------------------------------------------------------------
_client = None
_db = None


def get_client():
    """Get the MongoDB client (creates one if needed)."""
    global _client
    if _client is None:
        _client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        # Quick connectivity check
        try:
            _client.admin.command("ping")
            print(f"[DB] Connected to MongoDB at {MONGO_URI}")
        except Exception as e:
            print(f"[DB] WARNING: Could not connect to MongoDB: {e}")
    return _client


def get_db():
    """Get the honeypot database instance."""
    global _db
    if _db is None:
        _db = get_client()[DB_NAME]
        _ensure_indexes(_db)
    return _db


def _ensure_indexes(db):
    """Create indexes for fast queries (idempotent — safe to call repeatedly)."""
    # commands collection
    db.commands.create_index([("session_id", ASCENDING)])
    db.commands.create_index([("source_ip", ASCENDING)])
    db.commands.create_index([("timestamp", DESCENDING)])
    db.commands.create_index([("behavior_analysis.skill_level", ASCENDING)])

    # sessions collection
    db.sessions.create_index([("session_id", ASCENDING)], unique=True)
    db.sessions.create_index([("client_ip", ASCENDING)])
    db.sessions.create_index([("start_time", DESCENDING)])

    # session_replays collection
    db.session_replays.create_index([("session_id", ASCENDING)], unique=True)

    print("[DB] Indexes ensured on commands, sessions, session_replays")


def close_connection():
    """Close the MongoDB connection cleanly."""
    global _client, _db
    if _client:
        _client.close()
        _client = None
        _db = None
        print("[DB] Connection closed")
