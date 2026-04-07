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
import os

# Load .env file
load_dotenv()

# Get API key from .env
API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=API_KEY)

def chatbot():
    name = input("What's your name? ")
    print(f"Nice to meet you {name}!\n")

    # System instructions
    messages = [
        {
            "role": "system",
            "content": (
                "You are a friendly chatbot. Greet the user politely,"
                " ask how they are feeling (how are you), and respond naturally."
                " Like if they are happy >> positive reply, sad >> comforting them."
                " Do NOT repeat the username in every response."
            )
        }
    ]

    # Store conversation for saving to file
    conversation = []
    try:
        while True:
            user_input = input(">> ")

            # Exit condition
            if user_input.lower() in ["bye", "goodbye", "bie"]:
                goodbye_msg = f"Goodbye! {name}."
                print(goodbye_msg)
                conversation.append(f"User: {user_input}")
                conversation.append(f"Bot: {goodbye_msg}")
                break

            # Save user input
            conversation.append(f"User: {user_input}")
            messages.append({"role": "user", "content": user_input})

            # Call Groq API
            response = client.chat.completions.create(
                model='llama-3.1-8b-instant',
                messages=messages
            )

            # Get AI reply
            bot_reply = response.choices[0].message.content

            # Save AI reply
            messages.append({"role": "assistant", "content": bot_reply})
            conversation.append(f"Bot: {bot_reply}")

            # Print AI reply
            print(bot_reply)
    except KeyboardInterrupt:
        print(f"\nChat ended by user. Goodbye {name}!")
        conversation.append(f"Bot: Chat ended by user")            

    return conversation

# Run chatbot
conversation = chatbot()

# Save conversation to file
with open("smart_chatbot.txt", "w", encoding="utf-8") as file:
    for line in conversation:
        file.write(line + "\n")