"""
API Server for Honeypot Dashboard
Serves live data from honeypot_audit.json and session_recordings/
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime
from collections import Counter

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Paths
AUDIT_LOG_PATH = "honeypot_audit.json"
SESSION_RECORDINGS_PATH = "session_recordings"


def load_audit_logs():
    """Load all logs from honeypot_audit.json (NDJSON format)."""
    logs = []
    if os.path.exists(AUDIT_LOG_PATH):
        with open(AUDIT_LOG_PATH, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        logs.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    return logs


def get_session_recordings():
    """Get list of session recording files."""
    recordings = []
    if os.path.exists(SESSION_RECORDINGS_PATH):
        for filename in os.listdir(SESSION_RECORDINGS_PATH):
            if filename.endswith('.json'):
                filepath = os.path.join(SESSION_RECORDINGS_PATH, filename)
                try:
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                        recordings.append(data)
                except:
                    continue
    return recordings


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "ok", "timestamp": datetime.utcnow().isoformat() + "Z"})


@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    """Get dashboard metrics."""
    logs = load_audit_logs()
    
    # Count unique sessions
    sessions = set(log.get('session_id', '') for log in logs)
    active_sessions = len(sessions)
    
    # Count total commands
    total_commands = len(logs)
    
    # Count high-risk actions
    high_risk = sum(1 for log in logs 
                    if log.get('behavior_analysis', {}).get('skill_level') == 'High')
    
    # Calculate average session duration (placeholder)
    avg_duration = "12m 30s"
    
    return jsonify({
        "activeSessions": active_sessions,
        "totalCommands": total_commands,
        "highRiskActions": high_risk,
        "avgSessionDuration": avg_duration
    })


@app.route('/api/sessions', methods=['GET'])
def get_sessions():
    """Get list of all sessions with summary data."""
    logs = load_audit_logs()
    
    # Group logs by session
    session_data = {}
    for log in logs:
        session_id = log.get('session_id', 'unknown')
        if session_id not in session_data:
            session_data[session_id] = {
                'id': session_id,
                'ip': log.get('source_ip', 'unknown'),
                'country': 'Unknown',  # Would need GeoIP for real data
                'countryCode': 'UN',
                'username': log.get('username', 'unknown'),
                'skillLevel': 'Low',
                'riskLevel': 'Low',
                'startTime': log.get('timestamp', ''),
                'status': 'Ended',
                'commandCount': 0,
                'lastCommand': '',
                'commands': []
            }
        
        session_data[session_id]['commandCount'] += 1
        session_data[session_id]['lastCommand'] = log.get('command', {}).get('raw_input', '')
        session_data[session_id]['commands'].append(log)
        
        # Update skill level to highest seen
        skill = log.get('behavior_analysis', {}).get('skill_level', 'Low')
        if skill == 'High':
            session_data[session_id]['skillLevel'] = 'High'
            session_data[session_id]['riskLevel'] = 'Critical'
        elif skill == 'Medium' and session_data[session_id]['skillLevel'] != 'High':
            session_data[session_id]['skillLevel'] = 'Medium'
            session_data[session_id]['riskLevel'] = 'High'
    
    # Convert to list and sort by timestamp (most recent first)
    sessions = list(session_data.values())
    sessions.sort(key=lambda x: x['startTime'], reverse=True)
    
    return jsonify(sessions)


@app.route('/api/commands', methods=['GET'])
def get_commands():
    """Get list of all commands with details."""
    logs = load_audit_logs()
    
    commands = []
    for i, log in enumerate(reversed(logs)):  # Most recent first
        cmd = log.get('command', {})
        behavior = log.get('behavior_analysis', {})
        
        commands.append({
            'id': i + 1,
            'sessionId': log.get('session_id', ''),
            'timestamp': log.get('timestamp', ''),
            'command': cmd.get('raw_input', ''),
            'category': behavior.get('intent', 'Unknown'),
            'intent': behavior.get('intent', 'Unknown'),
            'skillLevel': behavior.get('skill_level', 'Low'),
            'output': ''  # Output not stored in current log format
        })
    
    # Limit to most recent 100
    return jsonify(commands[:100])


@app.route('/api/commands/frequency', methods=['GET'])
def get_command_frequency():
    """Get command frequency data for charts."""
    logs = load_audit_logs()
    
    # Count commands
    command_counts = Counter()
    for log in logs:
        cmd = log.get('command', {}).get('normalized', '').split()[0] if log.get('command', {}).get('normalized') else ''
        if cmd:
            command_counts[cmd] += 1
    
    # Get top 10
    top_commands = [
        {"name": cmd, "count": count, "category": "Command"}
        for cmd, count in command_counts.most_common(10)
    ]
    
    return jsonify(top_commands)


@app.route('/api/analytics/risk-distribution', methods=['GET'])
def get_risk_distribution():
    """Get risk level distribution for charts."""
    logs = load_audit_logs()
    
    # Count by skill level
    skill_counts = Counter(
        log.get('behavior_analysis', {}).get('skill_level', 'Low')
        for log in logs
    )
    
    total = len(logs) or 1
    
    distribution = [
        {"name": "Critical", "value": round(skill_counts.get('High', 0) / total * 100), "color": "#ef4444"},
        {"name": "High", "value": round(skill_counts.get('Medium', 0) / total * 50), "color": "#f97316"},
        {"name": "Medium", "value": round(skill_counts.get('Medium', 0) / total * 50), "color": "#eab308"},
        {"name": "Low", "value": round(skill_counts.get('Low', 0) / total * 100), "color": "#22c55e"}
    ]
    
    return jsonify(distribution)


@app.route('/api/analytics/timeline', methods=['GET'])
def get_timeline():
    """Get command timeline data for charts."""
    logs = load_audit_logs()
    
    # Group by hour
    hour_counts = Counter()
    for log in logs:
        timestamp = log.get('timestamp', '')
        if timestamp:
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                hour = dt.strftime('%H:00')
                hour_counts[hour] += 1
            except:
                continue
    
    # Create timeline data
    timeline = [
        {"time": hour, "commands": count}
        for hour, count in sorted(hour_counts.items())
    ]
    
    return jsonify(timeline)


@app.route('/api/analytics/skill-distribution', methods=['GET'])
def get_skill_distribution():
    """Get skill level distribution for heatmap."""
    logs = load_audit_logs()
    
    # Count by skill level
    skill_counts = Counter(
        log.get('behavior_analysis', {}).get('skill_level', 'Low')
        for log in logs
    )
    
    total = len(logs) or 1
    
    distribution = [
        {"name": "High", "value": round(skill_counts.get('High', 0) / total * 100), "color": "#ef4444"},
        {"name": "Medium", "value": round(skill_counts.get('Medium', 0) / total * 100), "color": "#f97316"},
        {"name": "Low", "value": round(skill_counts.get('Low', 0) / total * 100), "color": "#22c55e"}
    ]
    
    return jsonify(distribution)


@app.route('/api/session/<session_id>/replay', methods=['GET'])
def get_session_replay(session_id):
    """Get session replay data for a specific session."""
    logs = load_audit_logs()
    
    # Filter logs for this session
    session_logs = [log for log in logs if log.get('session_id') == session_id]
    
    # Convert to replay format
    replay_data = []
    for i, log in enumerate(session_logs):
        replay_data.append({
            'timestamp': i * 2000,  # 2 seconds apart
            'command': log.get('command', {}).get('raw_input', ''),
            'output': ''  # Would need to store outputs
        })
    
    return jsonify(replay_data)


@app.route('/api/recordings', methods=['GET'])
def get_recordings():
    """Get list of session recordings."""
    recordings = get_session_recordings()
    return jsonify(recordings)


if __name__ == '__main__':
    print("[*] Starting Honeypot API Server...")
    print("[*] API available at http://localhost:5000")
    print("[*] Endpoints:")
    print("    GET /api/health")
    print("    GET /api/metrics")
    print("    GET /api/sessions")
    print("    GET /api/commands")
    print("    GET /api/commands/frequency")
    print("    GET /api/analytics/risk-distribution")
    print("    GET /api/analytics/timeline")
    print("    GET /api/session/<id>/replay")
    app.run(host='0.0.0.0', port=5000, debug=True)
