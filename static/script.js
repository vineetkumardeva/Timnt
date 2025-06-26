const form = document.getElementById("recommend-form");
const resultDiv = document.getElementById("result");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const income = document.getElementById("income").value;
  const creditScore = document.getElementById("credit_score").value;

  const spending = {};
  document.querySelectorAll(".spending").forEach((cb) => {
    spending[cb.value] = cb.checked;
  });

  const benefits = Array.from(document.getElementById("benefits").selectedOptions).map(opt => opt.value);

  const payload = {
    income,
    spending,
    preferred_benefits: benefits,
    credit_score: creditScore || "unknown"
  };

  resultDiv.innerHTML = "⏳ Getting recommendations...";

  try {
    const res = await fetch("/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    if (data.recommendations && Array.isArray(data.recommendations)) {
      resultDiv.innerHTML = data.recommendations.map(card => `
        <div class="card-box">
          <img src="${card.image_url}" alt="${card.name}" />
          <h3>${card.name}</h3>
          <p><strong>Why it fits:</strong> ${card.reason}</p>
          <p><strong>Estimated Rewards:</strong> ${card.estimated_rewards}</p>
          <a href="${card.apply_link}" target="_blank">Apply Now</a>
        </div>
      `).join("");
    } else {
      resultDiv.innerHTML = `<pre>${data.recommendations}</pre>`;
    }

  } catch (err) {
    resultDiv.innerHTML = "❌ Error: " + err.message;
  }
});
const restartBtn = document.getElementById("restart-btn");

restartBtn.addEventListener("click", () => {
  form.reset();
  resultDiv.innerHTML = "";
});
