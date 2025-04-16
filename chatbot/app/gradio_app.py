import gradio as gr
import requests
import os 

# API_URL = "https://127.0.0.1:8000/chat"


API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
print(f"Using API URL: {API_URL}")


def chat_with_model(message, history):
    try:
        res = requests.post(f"{API_URL}/chat", json={"message": message})
        response = res.json()["response"]

    except Exception as e:
        response = f"Error: {str(e)}"   

    history.append((message, response))
    return history, history


def launch_app():
    with gr.Blocks() as app:
        gr.Markdown("## Chatbot")

        chatbot = gr.Chatbot()
        msg = gr.Textbox(placeholder="Type your message here...")
        clear = gr.Button("Clear")

        state = gr.State([])

        msg.submit(chat_with_model, [msg, state], [chatbot, state])
        clear.click(lambda: ([], []), outputs=[chatbot, state])

    app.launch()


if __name__ == "__main__":  
    launch_app()