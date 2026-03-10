from flask import Flask, render_template, request, jsonify
import datetime
import os
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# --- Firestore Initialization ---
# This part will be updated with actual credentials
# For now, we'll assume the credentials are set up via environment variables or a service account file
# More detailed instructions will be provided later for the user.
try:
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("Firestore initialized successfully using Application Default Credentials.")
except Exception as e:
    print(f"Error initializing Firestore: {e}")
    print("Please ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or running in a GCP environment.")
    db = None # Set db to None if initialization fails

APP_VERSION = os.environ.get("APP_VERSION", "1.0.0") # Default version

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/notes', methods=['POST'])
def add_note():
    if db is None:
        return jsonify({"error": "Firestore not initialized"}), 500

    note_content = request.json.get('content')
    if not note_content:
        return jsonify({"error": "Note content is required"}), 400

    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    note_data = {
        "content": note_content,
        "timestamp": timestamp,
        "app_version": APP_VERSION
    }

    try:
        doc_ref = db.collection('notes').add(note_data)
        return jsonify({"id": doc_ref[1].id, "message": "Note added successfully"}), 201
    except Exception as e:
        return jsonify({"error": f"Failed to add note: {e}"}), 500

@app.route('/notes', methods=['GET'])
def get_notes():
    if db is None:
        return jsonify({"error": "Firestore not initialized"}), 500

    try:
        notes_ref = db.collection('notes').order_by('timestamp', direction=firestore.Query.DESCENDING)
        notes = []
        for doc in notes_ref.stream():
            note = doc.to_dict()
            note['id'] = doc.id
            notes.append(note)
        return jsonify(notes), 200
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve notes: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
