from flask import Flask, request, render_template, jsonify
import openai
import os

app = Flask(__name__)

# Get API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY", "")

SYSTEM_PROMPT = (
    "You are an AI simulation of Steve Jobs. Respond to the user as Steve Jobs would. "
    "Maintain a visionary and inspirational tone. Include a disclaimer that you are an AI simulation, not the real Steve Jobs."
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({'response': 'Please enter a message.'})

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ]
        )
        reply = completion.choices[0].message["content"]
    except Exception as e:
        reply = f"Error: {e}"  # In production, handle errors more gracefully

    return jsonify({'response': reply})

if __name__ == '__main__':
    app.run(debug=True)
