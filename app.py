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
from songs import mood_songs_list
from food import food_chat
import os
import webbrowser

# Load API key
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=API_KEY)

def chatbot():
    # Ask name
    name = input("Hello! What's your name?\n")
    print(f"Hello {name}! Nice to meet you!\n")

    # Ask mood
    user_input = input("How are you feeling today?\n")
    mood = detect_mood(user_input)

    # Get 5 song suggestions
    songs = mood_songs_list(mood)
    if not songs:
        print("Sorry, no songs found for your mood.")
    else: 
        print("\nHere are some songs for your mood. Type the number you want:\n")
        for i, (title, _) in enumerate(songs, 1):
            print(f"{i}. {title}")

        # Let user pick a song
        while True:
            choice = input("\nEnter the number of the song you want (1-5): ")
            if choice.isdigit() and 1 <= int(choice) <= len(songs):
                choice = int(choice)
                song_title, song_url = songs[choice-1]
                break
            else:
                print("Invalid choice. Please try again.")

        print(f"\nPlaying: {song_title}")
        # webbrowser.open(song_url)

    # Initialize messages for Groq
    messages = [
        {"role": "system", "content": "You are a friendly chatbot. Greet naturally. Do NOT repeat the username."},
        {"role": "user", "content": user_input}
    ]
    conversation = [f"User: {user_input}"]

    # First bot reply
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages
    )
    bot_reply = response.choices[0].message.content
    print("\n" + bot_reply)
    messages.append({"role": "assistant", "content": bot_reply})
    conversation.append(f"Bot: {bot_reply}")

    # --- SWITCH TO FOOD-ONLY CHAT ---
    print("\n🍲 Now I will talk only about food. Ask me for recommendations!\n")
    while True:
        user_input = input(">> ")
        if user_input.lower() in ["bye", "goodbye", "bie"]:
            goodbye_msg = f"Goodbye {name}! 👋"
            print(goodbye_msg)
            conversation.append(f"User: {user_input}")
            conversation.append(f"Bot: {goodbye_msg}")
            break

        bot_reply = food_chat(client, messages, name, user_input)
        print(bot_reply)
        conversation.append(f"User: {user_input}")
        conversation.append(f"Bot: {bot_reply}")

    return conversation


if __name__ == "__main__":
    conversation = chatbot()
    with open("smart_chatbot.txt", "w", encoding="utf-8") as f:
        for line in conversation:
            f.write(line + "\n")