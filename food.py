def food_chat(client, messages, user_name, user_input):
    """
    Food-only chatbot (robust version)
    """

    # If first message → inject system role
    if not messages:
        messages.append({
            "role": "system",
            "content": """
            You are a food expert chatbot.

            Rules:
            - ONLY talk about food.
            - Suggest dishes, cuisines, recipes.
            - Keep answers short and helpful.
            - If NOT food-related → reply: I don't know
            """
        })

    # Add user message
    messages.append({
        "role": "user",
        "content": user_input
    })

    # Call model
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.7
    )

    bot_reply = response.choices[0].message.content.strip()

    # Safety fallback (VERY IMPORTANT)
    if not bot_reply or bot_reply.lower() in ["", "none"]:
        bot_reply = "Try something like: pizza, dosa, pasta, indian food 🍲"

    messages.append({
        "role": "assistant",
        "content": bot_reply
    })

    return bot_reply