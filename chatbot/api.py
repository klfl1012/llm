from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn
from mlx_lm import load, generate


# Inference
INIT_PROMPT = (
    "Du bist ein hochentwickelter KI-Schreibassistent, der professionelle, präzise und technische Texte "
    "in Deutsch und Englisch verfasst. Falls der Benutzer keine Sprache angibt, nutze die Sprache der Eingabe.\n\n"
)

model, tokenizer = load("fused_model")


def generate_response(prompt: str) -> str:
    full_prompt = INIT_PROMPT + prompt

    messages = [
        {"role": "user", "content": full_prompt},
    ]

    tokens = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        max_length=4000
    )

    response = generate(model, tokenizer, tokens)
    return response.strip()


def inference(prompt: str) -> str:
    try:
        return generate_response(prompt)
    except Exception as e:
        return f"Fehler bei der Inferenz: {str(e)}"

# FastAPI 
app = FastAPI()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str   


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    response = inference(request.message)
    return {"response": response}   

if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)





