"""
API Server for Honeypot Dashboard
==================================
Serves live data from MongoDB (honeypot_db).

Collections used:
  - commands        : Individual attacker commands
  - sessions        : Session metadata + analysis
  - session_replays : Full transcripts for replay
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
from database import get_db
from geoip_resolver import resolve_ip, is_private_ip

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend


# =========================================================================
# HEALTH CHECK
# =========================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    try:
        db = get_db()
        db.command("ping")
        return jsonify({
            "status": "ok",
            "database": "connected",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        })
    except Exception as e:
        return jsonify({
            "status": "degraded",
            "database": str(e),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }), 500


# =========================================================================
# DASHBOARD METRICS
# =========================================================================

@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    """Get dashboard metrics."""
    db = get_db()

    # Count unique sessions
    active_sessions = len(db.commands.distinct("session_id"))

    # Count total commands
    total_commands = db.commands.count_documents({})

    # Count high-risk actions
    high_risk = db.commands.count_documents({
        "behavior_analysis.skill_level": "High"
    })

    # Calculate average session duration from sessions collection
    pipeline = [
        {"$match": {"duration_seconds": {"$gt": 0}}},
        {"$group": {"_id": None, "avg_duration": {"$avg": "$duration_seconds"}}}
    ]
    result = list(db.sessions.aggregate(pipeline))
    if result:
        avg_secs = result[0]["avg_duration"]
        mins = int(avg_secs // 60)
        secs = int(avg_secs % 60)
        avg_duration = f"{mins}m {secs}s"
    else:
        avg_duration = "0m 0s"

    return jsonify({
        "activeSessions": active_sessions,
        "totalCommands": total_commands,
        "highRiskActions": high_risk,
        "avgSessionDuration": avg_duration
    })


# =========================================================================
# SESSIONS
# =========================================================================

@app.route('/api/sessions', methods=['GET'])
def get_sessions():
    """Get list of all sessions with summary data."""
    db = get_db()

    # Try sessions collection first (has rich data from SessionRecorder)
    sessions_from_db = list(db.sessions.find({}, {"_id": 0}).sort("start_time", -1))

    if sessions_from_db:
        # Format for frontend compatibility
        sessions = []
        for s in sessions_from_db:
            sessions.append({
                "id": s.get("session_id", ""),
                "ip": s.get("client_ip", "unknown"),
                "country": "Unknown",
                "countryCode": "UN",
                "username": s.get("username", "unknown"),
                "skillLevel": s.get("final_skill_level", "Low"),
                "riskLevel": "Critical" if s.get("final_skill_level") == "High" else
                             "High" if s.get("final_skill_level") == "Medium" else "Low",
                "startTime": s.get("start_time", ""),
                "status": "Ended" if s.get("end_time") else "Active",
                "commandCount": s.get("total_commands", 0),
                "lastCommand": s.get("last_command", "")
            })
        return jsonify(sessions)

    # Fallback: aggregate from commands collection
    pipeline = [
        {"$group": {
            "_id": "$session_id",
            "ip": {"$first": "$source_ip"},
            "username": {"$first": "$username"},
            "startTime": {"$first": "$timestamp"},
            "commandCount": {"$sum": 1},
            "lastCommand": {"$last": "$command.raw_input"},
            "skills": {"$push": "$behavior_analysis.skill_level"}
        }},
        {"$sort": {"startTime": -1}}
    ]
    results = list(db.commands.aggregate(pipeline))

    sessions = []
    for r in results:
        # Determine highest skill level
        skill = "Low"
        if "High" in r.get("skills", []):
            skill = "High"
        elif "Medium" in r.get("skills", []):
            skill = "Medium"

        sessions.append({
            "id": r["_id"],
            "ip": r.get("ip", "unknown"),
            "country": "Unknown",
            "countryCode": "UN",
            "username": r.get("username", "unknown"),
            "skillLevel": skill,
            "riskLevel": "Critical" if skill == "High" else "High" if skill == "Medium" else "Low",
            "startTime": r.get("startTime", ""),
            "status": "Ended",
            "commandCount": r.get("commandCount", 0),
            "lastCommand": r.get("lastCommand", "")
        })

    return jsonify(sessions)


# =========================================================================
# COMMANDS
# =========================================================================

@app.route('/api/commands', methods=['GET'])
def get_commands():
    """Get list of all commands with details (most recent 100)."""
    db = get_db()

    cursor = db.commands.find({}, {"_id": 0}).sort("timestamp", -1).limit(100)

    commands = []
    for i, log in enumerate(cursor):
        cmd = log.get("command", {})
        behavior = log.get("behavior_analysis", {})

        commands.append({
            "id": i + 1,
            "sessionId": log.get("session_id", ""),
            "timestamp": log.get("timestamp", ""),
            "command": cmd.get("raw_input", ""),
            "category": behavior.get("intent", "Unknown"),
            "intent": behavior.get("intent", "Unknown"),
            "skillLevel": behavior.get("skill_level", "Low"),
            "output": ""
        })

    return jsonify(commands)


@app.route('/api/commands/frequency', methods=['GET'])
def get_command_frequency():
    """Get command frequency data for charts."""
    db = get_db()

    pipeline = [
        {"$project": {
            "base_cmd": {
                "$arrayElemAt": [
                    {"$split": [{"$ifNull": ["$command.normalized", ""]}, " "]},
                    0
                ]
            }
        }},
        {"$match": {"base_cmd": {"$ne": ""}}},
        {"$group": {"_id": "$base_cmd", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]

    results = list(db.commands.aggregate(pipeline))

    top_commands = [
        {"name": r["_id"], "count": r["count"], "category": "Command"}
        for r in results
    ]

    return jsonify(top_commands)


# =========================================================================
# ANALYTICS
# =========================================================================

@app.route('/api/analytics/risk-distribution', methods=['GET'])
def get_risk_distribution():
    """Get risk level distribution for charts."""
    db = get_db()

    pipeline = [
        {"$group": {
            "_id": "$behavior_analysis.skill_level",
            "count": {"$sum": 1}
        }}
    ]
    results = list(db.commands.aggregate(pipeline))
    skill_counts = {r["_id"]: r["count"] for r in results}

    total = sum(skill_counts.values()) or 1

    distribution = [
        {"name": "Critical", "value": round(skill_counts.get("High", 0) / total * 100), "color": "#ef4444"},
        {"name": "High", "value": round(skill_counts.get("Medium", 0) / total * 50), "color": "#f97316"},
        {"name": "Medium", "value": round(skill_counts.get("Medium", 0) / total * 50), "color": "#eab308"},
        {"name": "Low", "value": round(skill_counts.get("Low", 0) / total * 100), "color": "#22c55e"}
    ]

    return jsonify(distribution)


@app.route('/api/analytics/timeline', methods=['GET'])
def get_timeline():
    """Get command timeline data for charts."""
    db = get_db()

    pipeline = [
        {"$match": {"timestamp": {"$ne": ""}}},
        {"$project": {
            "hour": {
                "$substr": ["$timestamp", 11, 5]
            }
        }},
        {"$group": {"_id": "$hour", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]

    results = list(db.commands.aggregate(pipeline))

    timeline = [
        {"time": r["_id"], "commands": r["count"]}
        for r in results
    ]

    return jsonify(timeline)


@app.route('/api/analytics/skill-distribution', methods=['GET'])
def get_skill_distribution():
    """Get skill level distribution for heatmap."""
    db = get_db()

    pipeline = [
        {"$group": {
            "_id": "$behavior_analysis.skill_level",
            "count": {"$sum": 1}
        }}
    ]
    results = list(db.commands.aggregate(pipeline))
    skill_counts = {r["_id"]: r["count"] for r in results}

    total = sum(skill_counts.values()) or 1

    distribution = [
        {"name": "High", "value": round(skill_counts.get("High", 0) / total * 100), "color": "#ef4444"},
        {"name": "Medium", "value": round(skill_counts.get("Medium", 0) / total * 100), "color": "#f97316"},
        {"name": "Low", "value": round(skill_counts.get("Low", 0) / total * 100), "color": "#22c55e"}
    ]

    return jsonify(distribution)


# =========================================================================
# SESSION REPLAY
# =========================================================================

@app.route('/api/session/<session_id>/replay', methods=['GET'])
def get_session_replay(session_id):
    """Get session replay data for a specific session."""
    db = get_db()

    replay = db.session_replays.find_one(
        {"session_id": session_id},
        {"_id": 0}
    )

    if replay and "transcript" in replay:
        replay_data = []
        for i, entry in enumerate(replay["transcript"]):
            replay_data.append({
                "timestamp": i * 2000,
                "command": entry.get("command", ""),
                "output": entry.get("output", "")
            })
        return jsonify(replay_data)

    # Fallback: build from commands collection
    commands = list(db.commands.find(
        {"session_id": session_id},
        {"_id": 0}
    ).sort("timestamp", 1))

    replay_data = []
    for i, cmd in enumerate(commands):
        replay_data.append({
            "timestamp": i * 2000,
            "command": cmd.get("command", {}).get("raw_input", ""),
            "output": ""
        })

    return jsonify(replay_data)


@app.route('/api/recordings', methods=['GET'])
def get_recordings():
    """Get list of session recordings."""
    db = get_db()

    recordings = list(db.session_replays.find({}, {"_id": 0}))
    return jsonify(recordings)


# =========================================================================
# GEO ATTACKS
# =========================================================================

@app.route('/api/attacks/geo', methods=['GET'])
def get_attacks_geo():
    """
    Get geographic location data for all attacker IPs.

    Aggregates data from commands collection, groups by IP,
    resolves each to geographic coordinates using GeoIP.
    """
    db = get_db()

    # Aggregate by IP
    pipeline = [
        {"$match": {"source_ip": {"$ne": "unknown"}}},
        {"$group": {
            "_id": "$source_ip",
            "timestamp": {"$first": "$timestamp"},
            "commandCount": {"$sum": 1},
            "sessions": {"$addToSet": "$session_id"},
            "skills": {"$push": "$behavior_analysis.skill_level"},
            "intents": {"$push": "$behavior_analysis.intent"}
        }}
    ]

    results = list(db.commands.aggregate(pipeline))

    geo_results = []
    for r in results:
        ip = r["_id"]

        # Determine highest skill level
        skill = "Low"
        if "High" in r.get("skills", []):
            skill = "High"
        elif "Medium" in r.get("skills", []):
            skill = "Medium"

        # Determine most dangerous attack type
        dangerous_intents = ["Privilege Escalation", "Exfiltration/Network", "Anti-Forensics"]
        attack_type = "Unknown"
        for intent in r.get("intents", []):
            if intent in dangerous_intents:
                attack_type = intent
                break

        # Resolve geo location
        geo = resolve_ip(ip)

        geo_results.append({
            "ip": ip,
            "country": geo["country"],
            "city": geo["city"],
            "latitude": geo["latitude"],
            "longitude": geo["longitude"],
            "timestamp": r.get("timestamp", ""),
            "attackType": attack_type,
            "commandCount": r.get("commandCount", 0),
            "skillLevel": skill,
            "sessionCount": len(r.get("sessions", [])),
            "isSimulated": geo.get("source") == "simulated"
        })

    # Sort by command count (most active first)
    geo_results.sort(key=lambda x: x["commandCount"], reverse=True)

    return jsonify(geo_results)


# =========================================================================
# RUN SERVER
# =========================================================================

if __name__ == '__main__':
    print("[*] Starting Honeypot API Server (MongoDB)...")
    print("[*] API available at http://localhost:5000")
    print("[*] Endpoints:")
    print("    GET /api/health")
    print("    GET /api/metrics")
    print("    GET /api/sessions")
    print("    GET /api/commands")
    print("    GET /api/commands/frequency")
    print("    GET /api/analytics/risk-distribution")
    print("    GET /api/analytics/timeline")
    print("    GET /api/analytics/skill-distribution")
    print("    GET /api/session/<id>/replay")
    print("    GET /api/recordings")
    print("    GET /api/attacks/geo")
    app.run(host='0.0.0.0', port=5000, debug=True)
