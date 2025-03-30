import os
import base64
import requests
import logging
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# API URLs
OLLAMA_URL = "http://localhost:11434/api/generate"
STABLE_DIFFUSION_URL = "http://127.0.0.1:7860/sdapi/v1/txt2img"

# Image Storage Path
IMAGE_SAVE_PATH = "static/images/generated"
os.makedirs(IMAGE_SAVE_PATH, exist_ok=True)

# Logging Setup
logging.basicConfig(level=logging.INFO)

def query_ollama(user_message):
    """Fetch AI response from Ollama API."""
    payload = {
        "model": "wizardlm2:7b",
        "prompt": user_message,
        "stream": False
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        return response.json().get("response", "Pepi didn't understand. Please try again.")
    except requests.exceptions.RequestException as e:
        return f"Error communicating with AI model: {e}"

def generate_image(prompt):
    """Generate an image using Stable Diffusion."""
    payload = {
        "prompt": prompt,
        "steps": 30,
        "cfg_scale": 7.5,
        "width": 512,
        "height": 512,
        "sampler_index": "Euler a"
    }
    try:
        response = requests.post(STABLE_DIFFUSION_URL, json=payload, timeout=60)
        response.raise_for_status()
        image_data = response.json().get("images", [None])[0]

        if image_data:
            image_bytes = base64.b64decode(image_data)
            image_filename = f"{prompt.replace(' ', '_')[:30]}.png"
            image_path = os.path.join(IMAGE_SAVE_PATH, image_filename)

            with open(image_path, "wb") as img_file:
                img_file.write(image_bytes)

            return f"/{image_path.replace(os.sep, '/')}"
        return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Error contacting Stable Diffusion: {e}")
        return None

@app.route("/")
def home():
    return render_template("index.html")

@socketio.on("send_message")
def handle_message(data):
    """Handles incoming chat messages."""
    user_message = data.get("message", "").strip()
    socketio.emit("receive_message", {"sender": "You", "message": user_message, "type": "text"})

    if user_message.lower().startswith("generate an image"):
        socketio.emit("receive_message", {"sender": "Pepi", "message": "Generating image...", "type": "status"})
        prompt = user_message.replace("generate an image", "").strip()
        image_path = generate_image(prompt)
        
        if image_path:
            socketio.emit("receive_message", {"sender": "Pepi", "message": image_path, "type": "image"})
        else:
            socketio.emit("receive_message", {"sender": "Pepi", "message": "Failed to generate image.", "type": "error"})
    else:
        bot_response = query_ollama(user_message)
        socketio.emit("receive_message", {"sender": "Pepi", "message": bot_response, "type": "text"})

if __name__ == "__main__":
    socketio.run(app, host="127.0.0.1", port=5000, debug=True)
