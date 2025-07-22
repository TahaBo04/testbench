from flask import Flask, request, jsonify
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

@app.route("/")
def index():
    return '''
    <h1>🧪 AI TestBench</h1>
    <form action="/chat" method="post" onsubmit="event.preventDefault(); fetchChat();">
      <input type="text" id="message" placeholder="Ask something..." style="width:300px">
      <button type="submit">Send</button>
    </form>
    <pre id="response"></pre>
    <script>
      async function fetchChat() {
        const msg = document.getElementById("message").value;
        const res = await fetch('/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: msg })
        });
        const data = await res.json();
        document.getElementById("response").textContent = data.reply;
      }
    </script>
    <p><em>Model: gpt-4</em></p>
    '''

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a concise and helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        reply = response.choices[0].message.content.strip()
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)