import os
from pydantic import SecretStr
import json
from flask import Flask, request, jsonify
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from flask import render_template

app = Flask(__name__)

# Load your credit cards from a static JSON file
with open('cards.json', 'r') as f:
    cards = json.load(f)

# Load Groq API key from environment variable (set in Replit secrets)
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize the LangChain Groq model
llm = ChatGroq(api_key=SecretStr(groq_api_key) if groq_api_key else None,
               model="llama3-70b-8192",
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


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/recommend", methods=["POST"])
def recommend_cards():
    user_data = request.json
    print("📥 Received user data:", user_data)

    try:
        formatted_prompt = prompt_template.format_messages(
            user_data=json.dumps(user_data),
            cards=json.dumps(cards)
        )

        # Get the LLM response
        response = llm.invoke(formatted_prompt)

        # Print response content to console
        print("🧠 LLM Response content:", response.content)

        # Return it to frontend
        return jsonify({"recommendations": response.content})

    except Exception as e:
        print("❌ Error generating recommendations:", str(e))
        return jsonify({"error": "Failed to generate recommendations"}), 500



# Run the Flask server (Replit-compatible)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
