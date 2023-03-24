"""
This module is the main entry point for the Echohive application.
It handles user input, sends requests to the OpenAI API, and processes the responses.
"""

import os
import sys
import openai
import tiktoken

# pip install openai tiktoken

# define your api key in your user environment variables. or here in the code
openai.api_key = os.getenv("OPENAI_API_KEY")


# Define the function to count tokens
def count_tokens(text):
    """
    This function performs a specific task, such as processing data,
    making a calculation, or interacting with an API.
    """
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    return len(encoding.encode(text))

# Set the maximum token limit
MAX_MEMORY_TOKENS = 50

# Initialize the conversation_history list
conversation_history = [
    {"role": "system", "content": "You are a helpful assistant."}
]

# The main loop for the chatbot
while True:
    # Get user input
    chat_input = input("You: ")

    # # Check if the user wants to print the entire chat history
    # if chat_input.lower() == "print chat history":
    #     print_chat_history = True
    # else:
    #     print_chat_history = False

    # Append user input to the conversation history
    conversation_history.append({"role": "user", "content": chat_input})
    # Calculate the total tokens in the conversation history
    total_tokens = sum(count_tokens(message["content"]) for message in conversation_history)
    print(f"Total tokens before removal: {total_tokens}")

    # Remove the oldest message from conversation history if total tokens exceed the maximum limit
    while total_tokens > MAX_MEMORY_TOKENS:
        if len(conversation_history) > 2:
            removed_message = conversation_history.pop(1)
            total_tokens -= count_tokens(removed_message["content"])
            # print total tokens used after removing the oldest message

        else:
            break
        print(f"Total tokens after removal: {total_tokens}")

    # Make API calls to OpenAI with the conversation history and use streaming responses
    print("About to send request")
    response = openai.ChatCompletion.create(
        model="gpt-4", # or gpt-3.5-turbo
        messages=conversation_history,
        stream=True,
    )
    print("Have the response!")

    # Process the response from the API
    for chunk in response:
        if "role" in chunk["choices"][0]["delta"]:
            continue

        elif "content" in chunk["choices"][0]["delta"]:
            r_text = chunk["choices"][0]["delta"]["content"]
            conversation_history.append({"role": "assistant", "content": r_text})
            sys.stdout.write(r_text)
            sys.stdout.flush()
    # new line after the assistant's response
    print()
