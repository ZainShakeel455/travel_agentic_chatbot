from flask import Flask, render_template, request, jsonify
from groq import Groq
import os
from dotenv import load_dotenv


load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = Flask(__name__)

def get_ai_response(user_input):
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role":"system",
                    "content": (
                        "You are SkyTravel's AI assistant."
                        "Answer customer queries about flights, hotels, holiday packages, timings, and policies."
                        "Be polite, concise, and helpfl."
                    ),
                },
                {"role": "user", "content": user_input},
            ],
            temperature=0.7,
            max_completion_tokens=300
        )

        return completion.choices[0].message.content
    
    except Exception as e:
        return f"⚠️ Error: {str(e)}"
    

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chatbot_response():
    user_message = request.json["message"]
    bot_response = get_ai_response(user_message)
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)
    