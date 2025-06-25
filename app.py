from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from transformers import pipeline
import uvicorn

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

model = pipeline("text2text-generation", model="google/flan-t5-large")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})

@app.post("/analyze", response_class=HTMLResponse)
async def analyze(request: Request, legal_text: str = Form(...)):
    prompt = f"""Classify the sentiment of the following legal document as Positive, Negative, or Neutral.\nThen, provide a one-sentence summary of its implication.\n\nText:\n\"\"\"{legal_text}\"\"\"\n\nOutput Format:\nSentiment: <Positive/Negative/Neutral>\nSummary: <Your summary here>"""
    result = model(prompt, max_length=256)[0]['generated_text']
    return templates.TemplateResponse("index.html", {"request": request, "result": result, "input": legal_text})