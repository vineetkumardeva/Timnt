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

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a credit card recommendation expert."),
    ("human",
     "User preferences: {user_data}\n\nFrom the list of credit cards below:\n{cards}\n\n"
     "Recommend the top 3 most suitable credit cards for the user. "
     "For each card, include:\n- Name\n- Short reason why it fits\n- Estimated yearly rewards (if possible)"
     )
])

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend_cards():
    user_data = request.json
    try:
        formatted_prompt = prompt_template.format_messages(
            user_data=json.dumps(user_data),
            cards=json.dumps(cards)
        )
        response = llm.invoke(formatted_prompt)
        return jsonify({"recommendations": response.content})
    except Exception as e:
        return jsonify({"error": "Failed to generate recommendations"}), 500

# Export the app for Vercel
# Do NOT run app.run()
