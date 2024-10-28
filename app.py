from flask import Flask, request, render_template, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configure the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_caption', methods=['POST'])
def generate_caption():
    # Check if the image and prompt are part of the request
    if 'file' not in request.files or 'prompt' not in request.form:
        return jsonify({"error": "No file or prompt provided"}), 400

    file = request.files['file']
    prompt = request.form['prompt']

    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Create a temporary file path to save the uploaded image
    temp_file_path = os.path.join('uploads', file.filename)
    os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)  # Ensure the uploads directory exists

    # Save the uploaded file to the temporary path
    file.save(temp_file_path)

    # Upload the file
    myfile = genai.upload_file(temp_file_path)

    # Create a model instance
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Generate content (Instagram caption)
    result = model.generate_content(
        [myfile, "\n\n", prompt]
    )

    # Clean up: remove the temporary file after processing
    os.remove(temp_file_path)

    # Return the generated caption
    return jsonify({"caption": result.text})

if __name__ == '__main__':
    app.run(debug=True)
