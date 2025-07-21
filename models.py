import torch
from transformers import Pipeline, pipeline

SYSTEM_PROMPT = (
"You are a helpful assistant. Answer clearly and reference only the provided context."
)
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def load_llm():
    return pipeline(
    "text-generation",
    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    torch_dtype=torch.bfloat16,
    device=DEVICE,
    )

def generate_answer(pipe: Pipeline, question: str, context: str, temperature=0.7):
    prompt = (
    f"{SYSTEM_PROMPT}\n\nContexto:\n{context}\n\n"
    f"Pregunta: {question}\nRespuesta:"
    )
    out = pipe(
    prompt,
    max_new_tokens=256,
    do_sample=True,
    temperature=temperature,
    top_p=0.95,
                )[0]["generated_text"]
    return out.split("Respuesta:")[-1].strip()