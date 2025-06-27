from flask import Flask, request, jsonify, render_template
import os
import json
from pydantic import SecretStr
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

app = Flask(__name__)

# Load cards
with open('cards.json', 'r') as f:
    cards = json.load(f)

groq_api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(api_key=SecretStr(groq_api_key) if groq_api_key else None,
               model="llama3-70b-8192",
               temperature=0.5,
               stop_sequences=None)

# Update: Prompt LLM to return JSON format
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a credit card recommendation expert."),
    ("human",
     "User preferences:\n{user_data}\n\n"
     "From the list of credit cards below:\n{cards}\n\n"
     "Recommend the top 3 most suitable credit cards for the user. "
     "Return a JSON array, where each item includes:\n"
     "- name\n- reason (short reason it fits)\n- estimated_rewards (e.g., 'Rs. 8000/year')\n"
     "- image_url\n- apply_link\n\n"
     "Respond ONLY with valid JSON.")
])

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/test-images")
def test_images():
    with open("cards.json") as f:
        cards = json.load(f)
    return render_template("test.html", cards=cards)


@app.route("/recommend", methods=["POST"])
def recommend_cards():
    user_data = request.json
    try:
        formatted_prompt = prompt_template.format_messages(
            user_data=json.dumps(user_data),
            cards=json.dumps(cards)
        )
        response = llm.invoke(formatted_prompt)

        # Ensure the content is valid JSON
        recommendations = json.loads(response.content)

        return jsonify({"recommendations": recommendations})
    except Exception as e:
        print("LLM error:", str(e))
        return jsonify({"error": "Failed to generate recommendations"}), 500
