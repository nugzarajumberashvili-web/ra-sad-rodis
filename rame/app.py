import os
import sys
import uuid
from flask import Flask, render_template, request, jsonify, send_from_directory

# Fix Windows console encoding
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

import model

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = os.environ.get("FLASK_SECRET", "ai_multiagent_squad_key_2026")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/favicon.ico")
def favicon():
    return ('', 204)

@app.route("/api/agents", methods=["GET"])
def get_agents():
    """Returns the list and metadata of squad agents."""
    agents_data = []
    for k, v in model.AGENTS.items():
        agents_data.append({
            "id": v["id"],
            "name": v["name"],
            "role": v["role"],
            "role_ka": v["role_ka"],
            "avatar": v["avatar"],
            "color": v["color"],
            "glow": v["glow"],
            "gradient": v["gradient"],
            "badge": v["badge"],
            "specialty": v["specialty"],
            "specialty_ka": v["specialty_ka"],
            "sample_prompts": v["sample_prompts"]
        })
    return jsonify({"success": True, "agents": agents_data})

@app.route("/api/chat", methods=["POST"])
def chat():
    """Direct conversation with an agent."""
    data = request.get_json(force=True, silent=True) or {}
    message = data.get("message", "").strip()
    agent_id = data.get("agent", "auto")
    session_id = data.get("sessionId") or str(uuid.uuid4())

    if not message:
        return jsonify({"success": False, "error": "Message is required"}), 400

    # Auto-routing if agent is set to 'auto'
    if agent_id == "auto":
        agent_id = model.smart_route(message)

    try:
        reply = model.ask_agent(agent_id, message, session_id=session_id)
        return jsonify({
            "success": True,
            "agent": agent_id,
            "agent_meta": {
                "name": model.AGENTS[agent_id]["name"],
                "avatar": model.AGENTS[agent_id]["avatar"],
                "color": model.AGENTS[agent_id]["color"]
            },
            "response": reply,
            "sessionId": session_id
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/syndicate", methods=["POST"])
def syndicate():
    """Multi-Agent Syndicate round-table discussion."""
    data = request.get_json(force=True, silent=True) or {}
    message = data.get("message", "").strip()
    session_id = data.get("sessionId") or str(uuid.uuid4())

    if not message:
        return jsonify({"success": False, "error": "Topic is required"}), 400

    try:
        result = model.syndicate_discuss(message, session_id=session_id)
        return jsonify({
            "success": True,
            "data": result,
            "sessionId": session_id
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/quiz", methods=["POST"])
def quiz():
    """Generates an interactive multiple-choice quiz question."""
    data = request.get_json(force=True, silent=True) or {}
    subject = data.get("subject", "mixed")
    lang = data.get("lang", "ka")

    try:
        q_data = model.generate_quiz(subject, lang=lang)
        return jsonify({"success": True, "quiz": q_data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/reset", methods=["POST"])
def reset():
    """Resets conversation history."""
    data = request.get_json(force=True, silent=True) or {}
    session_id = data.get("sessionId", "default")
    agent_id = data.get("agent", "all")

    if agent_id == "all":
        model.reset_all_sessions(session_id)
    else:
        model.reset_agent(agent_id, session_id)

    return jsonify({"success": True, "message": "Memory reset successfully"})

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "service": "Multi-Agent AI Intelligence Hub"})

if __name__ == "__main__":
    print("🚀 AI Multi-Agent Server starting on http://127.0.0.1:5000 ...")
    app.run(host="127.0.0.1", port=5000, debug=False)
