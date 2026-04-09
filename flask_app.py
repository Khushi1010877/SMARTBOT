from flask import Flask, render_template, request, jsonify
import app
from food import food_chat
import webbrowser

flask_app = Flask(__name__)

# Session state
session_state = {
    "stage": "ask_name",
    "name": None,
    "songs": [],
    "messages": []
}

@flask_app.route("/")
def index():
    return render_template("index.html")

@flask_app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").strip()

    # Exit condition
    if user_input.lower() in ["bye", "goodbye", "bie"]:
        name = session_state.get("name") or ""
        session_state.update({
            "stage": "ask_name",
            "name": None,
            "songs": [],
            "messages": []
        })
        return jsonify({"reply": f"Goodbye {name}! 👋"})

    # ------------------ STAGE 1 ------------------
    if session_state["stage"] == "ask_name":
        session_state["name"] = user_input
        session_state["stage"] = "ask_mood"
        return jsonify({"reply": f"Hello {user_input}! How are you feeling today?"})

    # ------------------ STAGE 2 ------------------
    elif session_state["stage"] == "ask_mood":
        songs = app.mood_songs_list(user_input)
        session_state["songs"] = songs
        session_state["stage"] = "song_selection"

        if not songs:
            return jsonify({"reply": "Sorry, no songs found."})

        reply = "Here are some songs for your mood:\n"
        for i, (title, _) in enumerate(songs, 1):
            reply += f"{i}. {title}\n"

        return jsonify({"reply": reply})

    # ------------------ STAGE 3 ------------------
    elif session_state["stage"] == "song_selection":

        # If valid number → go to food mode
        if user_input.isdigit() and 1 <= int(user_input) <= len(session_state["songs"]):
            idx = int(user_input) - 1
            song_title, song_url = session_state["songs"][idx]

            webbrowser.open(song_url)

            session_state["stage"] = "specialized_chat"
            session_state["messages"] = [ {
                                            "role": "system",
                                            "content": """
                                            You are a food expert chatbot.
                                            Only talk about food.
                                            If not food → say: I don't know
                                            """
                                            }]  # reset chat history

            return jsonify({
                "reply": f"Playing: {song_title}\nNow I will only talk about food. 🍲"
            })

        # EVEN if user types anything else → still switch to food mode
        session_state["stage"] = "specialized_chat"
        session_state["messages"] = []

        return jsonify({
            "reply": "Now I will only talk about food. Ask me something! 🍕"
        })

    # ------------------ STAGE 4 (FOOD MODE) ------------------
    elif session_state["stage"] == "specialized_chat":
        bot_reply = food_chat(
            app.client,
            session_state["messages"],
            session_state["name"],
            user_input
        )

        return jsonify({"reply": bot_reply})

# Run app
if __name__ == "__main__":
    flask_app.run(debug=True)
