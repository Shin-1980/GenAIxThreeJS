import os
import json
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from openai import OpenAI  
from datetime import datetime

api_key = ""
model = ""

if not api_key:
    raise ValueError("ERROR: OPENAI_API_KEY is not set")

if not model:
    raise ValueError("ERROR: Model is not set")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Create FastAPI app
app = FastAPI()

# Enable CORS (so frontend can access the backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Default fallback Three.js script
three_js_script = """
const geometry = new THREE.BoxGeometry();
const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
const cube = new THREE.Mesh(geometry, material);
cube.position.set(0, 0, 0);
scene.add(cube);
"""

# Generate Three.js code from OpenAI
def generate_three_js_code(user_command: str):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": (
                    "You are a JavaScript coding assistant. "
                    "ONLY return valid Three.js object creation code. "
                    "follow below formats as an example"
                    "const geometry = new THREE.BoxGeometry();"
                    "const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });"
                    "const cube = new THREE.Mesh(geometry, material);"
                    "cube.position.set(0, 0, 0);"
                    "scene.add(cube);"
                    "DO NOT redeclare `scene`, `camera`, or `renderer`."
                    "DO NOT generate ```javascript before script"
                    "DO NOT generate ```after script"
                )},
                {"role": "user", "content": f"Create a Three.js scene with: {user_command}"}
            ],
            max_tokens=300,
            temperature=0.5
        )

        generated_code = response.choices[0].message.content.strip()

        if not generated_code or "scene.add" not in generated_code:
            print("AI returned an invalid script. Replacing with default object.")
            return 'console.error("AI-generated script was invalid.");'

        return generated_code

    except Exception as e:
        print(f"OpenAI API Error: {e}")
        return 'console.error("OpenAI failed to generate a script.");'

# Endpoint to get the current script
@app.get("/get_script")
def get_script():
    return JSONResponse(content={"script": three_js_script.strip()})

# Endpoint to update script based on user command
@app.post("/update_script")
async def update_script(request: Request):
    global three_js_script
    data = await request.json()
    user_command = data.get("command", "").strip()

    if not user_command:
        return JSONResponse(content={"status": "error", "message": "No command provided."}, status_code=400)

    print(f"Received command: {user_command}")

    generated_code = generate_three_js_code(user_command)

    if not generated_code:
        return JSONResponse(content={"status": "error", "message": "Failed to generate script."}, status_code=500)

    three_js_script = generated_code
    print(three_js_script)

   # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"history/scene_{timestamp}.json"
    with open(filename, "w") as f:
        json.dump({"command": user_command, "script": three_js_script}, f, indent=2)

    return JSONResponse(content={"status": "updated", "script": generated_code})
