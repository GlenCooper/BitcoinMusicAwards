#!/usr/bin/env python3

# app.py for BitcoinMusicAwards
# by 1GLENCo (https://1glenco.com)
# https://www.perplexity.ai/search/i-have-a-python-script-on-my-l-HdmHzQz9QJy6ZGG_8Z2fmw

import hashlib
from datetime import datetime, timezone

# Storage simulation (will move to persistent storage later)
storage = {
    "admin": {},
    "polls": {},
    "votes": {}
}

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def set_master_password(password: str) -> str:
    if "password_hash" in storage["admin"]:
        return "Master password already set."
    storage["admin"]["password_hash"] = hash_password(password)
    return "Master password set successfully."

def verify_master_password(password: str) -> bool:
    if "password_hash" not in storage["admin"]:
        return False
    return storage["admin"]["password_hash"] == hash_password(password)

# Create Poll Example
poll_id = "poll1"
storage["polls"][poll_id] = {
    "title": "Best New Bitcoin Music Producer",
    "end_date": datetime(2025, 8, 31, 23, 59, 59, tzinfo=timezone.utc).isoformat(),
    "candidates": [],
    "votes": {}
}

def add_candidate(poll_id: str, candidate_id: str, candidate_name: str) -> str:
    poll = storage["polls"].get(poll_id)
    if not poll:
        return "Poll not found."
    if candidate_id in poll["candidates"]:
        return "Candidate already exists."
    poll["candidates"].append(candidate_id)
    storage["votes"][candidate_id] = { "name": candidate_name, "vote_count": 0 }
    return f"Candidate '{candidate_name}' added to poll."

def cast_vote(poll_id: str, voter_id: str, candidate_id: str) -> str:
    poll = storage["polls"].get(poll_id)
    if not poll:
        return "Poll not found."
    if datetime.now(timezone.utc) > datetime.fromisoformat(poll["end_date"]):
        return "Poll has ended."
    if candidate_id not in poll["candidates"]:
        return "Invalid candidate."
    if voter_id in poll["votes"]:
        return "You have already voted."
    poll["votes"][voter_id] = candidate_id
    storage["votes"][candidate_id]["vote_count"] += 1
    return "Vote cast successfully."

def get_poll_results(poll_id: str):
    poll = storage["polls"].get(poll_id)
    if not poll:
        return "Poll not found."
    results = [{"candidate": storage["votes"][cid]["name"], "votes": storage["votes"][cid]["vote_count"]} for cid in poll["candidates"]]
    results.sort(key=lambda x: x["votes"], reverse=True)
    return results
