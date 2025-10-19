from flask import Flask, request
import requests
import json

app = Flask(__name__)

ACCESS_TOKEN = "EAAWoxeqcVxYBPuDOOMaTVZCifPWwI1ZChTvkq3wLun6DD2oFWKjBm1AqeZBo7beeYE7Y7j8mZA0SrgFdS7vMI4gmKeckBOkEAsHjbYplGZChClOF4nC75vEqeN0vcqRZAsQEUZBEcMSkHPUYZAEZCLhc7D00AcJekBLZAYtWbXAQWGGXZCcOhrHvtoUz9Wmp3h8CHDTVJgVMluS0gY8BaNvLqm1wGDmZB6BiAcNndg8DZBwHjwNh01gZDZD"
PHONE_NUMBER_ID = "843944528799415"
VERIFY_TOKEN = "mywhatsapptoken"

@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge
    return "Verification failed", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("📩 Received webhook data:")
    print(json.dumps(data, indent=2))  # <-- log everything

    try:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        from_number = message["from"]
        text = message["text"]["body"]

        if "hi" in text.lower():
            reply = "Hello! 👋 How can I help you today?"
        else:
            reply = "Thanks for your message! I'll get back to you soon."

        url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json",
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": from_number,
            "type": "text",
            "text": {"body": reply},
        }
        response = requests.post(url, headers=headers, json=payload)
        print("✅ Sent reply:", response.text)

    except Exception as e:
        print("❌ Error handling webhook:", e)

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

