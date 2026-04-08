"""
we will build a simple but smart chatbot.*

Your chatbot will:

1. Ask for the user’s name and remember it
2. Talk to the user (hello, how are you)
    If user says:
        hi / hello
    Bot:
        Hello userName!
3. Understand the user’s feelings (happy/sad)  
    If user says:
        "I am sad" → comforting reply
        "I am happy" → positive reply
4. Exit politely
    If user says "bye"
    Bot:
        Goodbye Riya!"""


from groq import Groq
from dotenv import load_dotenv
from moods import detect_mood
from songs import mood_songs_list  # updated function
import os
import webbrowser

# Load API key
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=API_KEY)

def chatbot():
    # Ask name
    name = input("What's your name? ")
    print(f"Nice to meet you {name}!\n")

    # Ask mood
    user_input = input("How are you feeling today? ")
    mood = detect_mood(user_input)

    # Get 5 song suggestions
    songs = mood_songs_list(mood)
    if not songs:
        print("Sorry, no songs found for your mood.")
        song_url = None
    else:
        print("\nHere are some songs for your mood:")
        for i, (title, _) in enumerate(songs, 1):
            print(f"{i}. {title}")

        # Let user pick a song
        while True:
            choice = input("\nEnter the number of the song you want for recommendation (1-5): ")
            if choice.isdigit() and 1 <= int(choice) <= len(songs):
                choice = int(choice)
                song_title, song_url = songs[choice-1]
                break
            else:
                print("Invalid choice. Please try again.")

        print(f"\nPlaying: {song_title}")
        webbrowser.open(song_url)

    # Initialize Groq conversation
    messages = [
        {
            "role": "system",
            "content": (
                "You are a friendly chatbot. Greet the user politely, "
                "ask how they are feeling, and respond naturally. "
                "Do NOT repeat the username in every response."
            )
        },
        {"role": "user", "content": user_input}
    ]
    conversation = [f"User: {user_input}"]

    # Call Groq API for first reply
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages
    )
    bot_reply = response.choices[0].message.content
    print("\n" + bot_reply)
    messages.append({"role": "assistant", "content": bot_reply})
    conversation.append(f"Bot: {bot_reply}")

    # Continue chatting
    while True:
        user_input = input(">> ")
        if user_input.lower() in ["bye", "goodbye", "bie"]:
            goodbye_msg = f"Goodbye {name}! 👋"
            print(goodbye_msg)
            conversation.append(f"User: {user_input}")
            conversation.append(f"Bot: {goodbye_msg}")
            break

        conversation.append(f"User: {user_input}")
        messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages
        )
        bot_reply = response.choices[0].message.content
        print(bot_reply)
        messages.append({"role": "assistant", "content": bot_reply})
        conversation.append(f"Bot: {bot_reply}")

    return conversation


if __name__ == "__main__":
    conversation = chatbot()

    with open("smart_chatbot.txt", "w", encoding="utf-8") as f:
        for line in conversation:
            f.write(line + "\n")