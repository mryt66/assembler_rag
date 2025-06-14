import requests
import json

SERVER_URL = "http://127.0.0.1:8000/chat" # Ensure this matches your local server address

def run_chat_loop():
    history = []
    print("Starting chat session with the RAG application.")
    print("The server in \'main.py\' must be running in another terminal.")
    print("Type your message and press Enter. Type \'quit\' or \'exit\' to end.")
    print("-" * 30)

    while True:
        try:
            user_input = input("You: ")
        except KeyboardInterrupt:
            print("\\nExiting chat due to KeyboardInterrupt.")
            break
        
        if user_input.lower() in ["quit", "exit"]:
            print("Exiting chat.")
            break

        history.append({"role": "user", "message": user_input})

        try:
            response = requests.post(SERVER_URL, json={"history": history})
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
            
            response_data = response.json()
            assistant_response = response_data.get("response")

            if assistant_response:
                print(f"Assistant: {assistant_response}")
                history.append({"role": "assistant", "message": assistant_response})
            else:
                print("Assistant: Received no valid response content.")
                # If the server didn't process the message well, remove the last user input from history
                # to avoid sending a broken history next time.
                if history and history[-1]["role"] == "user":
                    history.pop()
        
        except requests.exceptions.ConnectionError:
            print(f"Error: Could not connect to the server at {SERVER_URL}.")
            print("Please ensure \'main.py\' is running.")
            # Remove the last user input as it wasn't processed
            if history and history[-1]["role"] == "user":
                history.pop()
            # break # You might want to break the loop if connection fails repeatedly
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error from server: {e}")
            print(f"Response content: {response.text}") # Show more details from server
            if history and history[-1]["role"] == "user":
                history.pop()
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with the server: {e}")
            if history and history[-1]["role"] == "user":
                history.pop()
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON response from the server. Response: {response.text}")
            if history and history[-1]["role"] == "user":
                history.pop()
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            if history and history[-1]["role"] == "user":
                history.pop()

if __name__ == "__main__":
    run_chat_loop()
