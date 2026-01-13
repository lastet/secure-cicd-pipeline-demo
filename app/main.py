from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict
import html
import uuid

app = FastAPI(title="Secure CI/CD Demo")

# In-memory storage 
NOTES: Dict[str, str] = {}

class NoteCreate(BaseModel):
    # ограничим длину — это уже “security-minded” validation
    text: str = Field(min_length=1, max_length=280)

class NoteOut(BaseModel):
    id: str
    text: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/hello")
def hello(name: str = "world"):
    return {"message": f"hello, {name}"}

@app.post("/notes", response_model=NoteOut, status_code=201)
def create_note(payload: NoteCreate):
   
    safe_text = html.escape(payload.text)
    note_id = str(uuid.uuid4())
    NOTES[note_id] = safe_text
    return {"id": note_id, "text": safe_text}

@app.get("/notes", response_model=list[NoteOut])
def list_notes():
    return [{"id": nid, "text": txt} for nid, txt in NOTES.items()]

@app.get("/notes/{note_id}", response_model=NoteOut)
def get_note(note_id: str):
    if note_id not in NOTES:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"id": note_id, "text": NOTES[note_id]}

@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: str):
    if note_id not in NOTES:
        raise HTTPException(status_code=404, detail="Note not found")
    del NOTES[note_id]
    return None
