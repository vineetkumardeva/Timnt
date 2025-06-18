import os
from pydantic import SecretStr
import json
from flask import Flask, request, jsonify
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

app = Flask(__name__)

# Load your credit cards from a static JSON file
with open('cards.json', 'r') as f:
    cards = json.load(f)

# Load Groq API key from environment variable (set in Replit secrets)
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize the LangChain Groq model
llm = ChatGroq(api_key=SecretStr(groq_api_key) if groq_api_key else None,
               model="mixtral-8x7b-32768",
               temperature=0.5,
               stop_sequences=None)

# Create a structured prompt using LangChain's ChatPromptTemplate
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a credit card recommendation expert."),
    ("human",
     "User preferences: {user_data}\n\nFrom the list of credit cards below:\n{cards}\n\n"
     "Recommend the top 3 most suitable credit cards for the user. "
     "For each card, include:\n- Name\n- Short reason why it fits\n- Estimated yearly rewards (if possible)"
     )
])


@app.route("/recommend", methods=["POST"])
def recommend_cards():
    user_data = request.json

    formatted_prompt = prompt_template.format_messages(
        user_data=json.dumps(user_data), cards=json.dumps(cards))

    response = llm.invoke(formatted_prompt)

    return jsonify({"recommendations": response.content})

@app.route("/", methods=["GET"])
def hello():
    return "✅ Credit Card Recommender API is running. Use POST /recommend with JSON data."

# Run the Flask server (Replit-compatible)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)


