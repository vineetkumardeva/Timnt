# Credit Card Recommender (LLM-Powered Prototype)

A conversational credit card recommendation web app built with Flask,LangChain + Groq LLM, and a static cards database.  
It collects user preferences via a simple webpage and suggests the top 3 cards tailored to their needs.

DEPLOYED LINK = https://timnt.vercel.app/
DEMO = https://drive.google.com/file/d/10efx1giKn7ggYC_F7pkUvS7AjI_Kdx-E/view?usp=sharing

WORKING:-

1.Frontend  
   - A one-page form (`index.html`) asks for:
     - Monthly income
     - Spending habits (fuel, travel, groceries)
     - Preferred benefits (cashback, lounge access)
     - Credit score  
   - On form submission, it sends data to the backend via `/recommend`.

2.Backend  
   - Built with Flask(`main.py`) and serves routes:
     - `GET /` → serves the form
     - `POST /recommend` → processes user data
   - Loads `cards.json` containing 20 Indian credit cards with details (name, issuer, fees, perks).
   - Uses **LangChain** and **ChatGroq** (`llama3-70b-8192`) to:
     - Build a prompt combining user preferences and available cards
     - Generate the top 3 personalized recommendations

3.Output  
   - The LLM returns recommendations with:
     - Card name
     - Reason for fit
     - Estimated yearly rewards  
   - Shown to the user on the same page.

---

Tech Stack
- Python + Flask
- LangChain with ChatGroq (Groq LLM API)
- Groq model: `llama3-70b-8192` 
- Static card data via `cards.json`
- Frontend: HTML, CSS, JavaScript

Installation & Run

```bash
git clone https://github.com/vineetkumardeva/Timnt.git
cd Timnt
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```


Agent Flow:-

1.User Input (Frontend):-
   * User fills out the form with details like monthly income, spending categories, preferred benefits, and credit score.
   * The form data is sent as JSON via a POST request to the `/recommend` API endpoint.

2.Backend Processing (Flask):
   * The Flask app receives the JSON input.
   * Loads static credit card data from `cards.json`.
   * Constructs a prompt by combining user data and credit card details.

3.LLM Invocation (LangChain + ChatGroq):
   * Uses `ChatGroq` LLM model (`llama3-70b-8192`) from Groq API.
   * The prompt instructs the LLM to act as a credit card recommendation expert.
   * LLM processes the input and returns the top 3 card recommendations with reasons and estimated yearly rewards.

4. Response to Frontend:
   * Flask sends the LLM’s response back as JSON.
   * Frontend displays the recommendations to the user.

Prompt Design - The prompt uses `ChatPromptTemplate` with two messages:
* **System message:**
  *"You are a credit card recommendation expert."*

* **Human message:**

  ```
  User preferences: {user_data}

  From the list of credit cards below:
  {cards}

  Recommend the top 3 most suitable credit cards for the user.
  For each card, include:
  - Name
  - Short reason why it fits
  - Estimated yearly rewards (if possible)
  ```

`{user_data}` and `{cards}` are JSON strings dynamically inserted from the input and static data.

This structured prompt guides the model to produce concise, relevant credit card recommendations personalized for the user’s needs.
