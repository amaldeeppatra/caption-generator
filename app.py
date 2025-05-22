from flask import Flask, request, render_template, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

load_dotenv()
app = Flask(__name__)

# Configure the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_caption', methods=['POST'])
def generate_caption():
    if 'file' not in request.files or 'notes' not in request.form or 'platform' not in request.form:
        return jsonify({"error": "Missing file, notes, or platform"}), 400
    
    file = request.files['file']
    notes = request.form['notes']
    platform = request.form['platform']
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    upload_dir = 'uploads'
    os.makedirs(upload_dir, exist_ok=True)
    temp_path = os.path.join(upload_dir, file.filename)
    file.save(temp_path)
    
    myfile = genai.upload_file(temp_path)
    
    # Check if platform needs song suggestion
    needs_song = platform.lower() in ['instagram', 'facebook']
    
    if needs_song:
        # Enhanced prompt for platforms that support music
        master_prompt = (
            "You are a social media content creator expert. Analyze the provided image and generate content for {platform}.\n\n"
            "Your response must be in this exact JSON format:\n"
            "{{\n"
            '  "caption": "Your {platform} caption here",\n'
            '  "song_suggestion": {{\n'
            '    "title": "Song Title",\n'
            '    "artist": "Artist Name",\n'
            '    "reason": "Brief explanation why this song fits the image/mood"\n'
            '  }}\n'
            "}}\n\n"
            "Requirements:\n"
            "1. Generate an engaging {platform} caption suitable for the image\n"
            "2. Suggest a popular song that matches the mood, theme, or vibe of the image\n"
            "3. Consider the user's additional notes: {notes}\n"
            "4. The song should be well-known and available on major streaming platforms\n"
            "5. Provide a brief reason why the song fits\n"
            "6. Return ONLY the JSON, no additional text"
        )
    else:
        # Standard prompt for other platforms
        master_prompt = (
            "You are a social media caption generator. "
            "Generate a {platform} caption for the provided image. "
            "Include only the caption in the response, no additional text. "
            "Additional notes: {notes}"
        )
    
    full_prompt = master_prompt.format(platform=platform.capitalize(), notes=notes or "No additional notes")
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    result = model.generate_content([myfile, "\n\n", full_prompt])
    
    # Clean up uploaded file
    os.remove(temp_path)
    
    try:
        if needs_song:
            # Try to parse JSON response
            response_text = result.text.strip()
            # Remove markdown code blocks if present
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()
            elif response_text.startswith('```'):
                response_text = response_text.replace('```', '').strip()
            
            response_data = json.loads(response_text)
            return jsonify(response_data)
        else:
            # Standard response for platforms without song suggestions
            return jsonify({"caption": result.text.strip()})
    
    except json.JSONDecodeError:
        # Fallback if JSON parsing fails
        if needs_song:
            return jsonify({
                "caption": result.text.strip(),
                "song_suggestion": {
                    "title": "Perfect",
                    "artist": "Ed Sheeran",
                    "reason": "A versatile song that fits many moods and moments"
                }
            })
        else:
            return jsonify({"caption": result.text.strip()})
    
    except Exception as e:
        return jsonify({"error": f"Error generating content: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8050, host='0.0.0.0')