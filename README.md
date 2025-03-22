# 3D rendering automated by OpenAI

This website automatically generate 3D rendering from high-level natural language by communicating with OpenAI.
A command of a natural language is entered into a text box at the top of the website, and clicking "Modify scene" button triggers a message to a server ("app.py"). The server interprets the command and dynamically generates the corresponding Three.js script. The new scripts are fetched on the client, and the 3D view is instantly updated. 

## Protocol to OpenAI

* OpenAI requires OpenAI API key, the model of OpenAI, and messages.

* The message defines the conversation history sent to the model. 

In this code, the message contains a role of OpenAI, task & restrictions, examples, prohibited conditions, and user command.

  ```Python
            messages=[
                {"role": "system", "content": (
                    # a role of OpenAI
                    "You are a JavaScript coding assistant. "
                    # task & restrictions
                    "ONLY return valid Three.js object creation code. "
                    # examples
                    "follow below formats as an example"
                    "const geometry = new THREE.BoxGeometry();"
                    "const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });"
                    "const cube = new THREE.Mesh(geometry, material);"
                    "cube.position.set(0, 0, 0);"
                    "scene.add(cube);"
                    # prohibited conditions
                    "DO NOT redeclare `scene`, `camera`, or `renderer`."
                    "DO NOT generate ```javascript before script"
                    "DO NOT generate ```after script"
                )},
                # user command
                {"role": "user", "content": f"Create a Three.js scene with: {user_command}"}
            ],
  ```

## How to run

First, open a terminal to execute the following code to run a FastAPI web application using Uvicorn, an ASGI web server. 

<pre><code>```
cd GenAIxThreeJS
uvicorn app:app --reload; 
``` </code></pre>

Second, open another terminal to run the following command telling Node.js to run a custom script named dev that's defined in the project's

<pre><code>```
npm run dev
``` </code></pre>

Finally, open web brouser, and enter http://localhost:5173/ to an address bar, which result in opening the website displaying 3D model.

  
