import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

DATA_FILE = Path(__file__).parent / "data.json"

app = FastAPI(title="Mock CVR API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Virksomhed(BaseModel):
    firmanavn: str
    adresse: str
    postnummer: str
    by: str


def load_data() -> dict:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data: dict) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/cvr")
def get_alle_virksomheder():
    return load_data()


@app.get("/cvr/{cvr_nummer}")
def get_virksomhed(cvr_nummer: str):
    data = load_data()
    if cvr_nummer not in data:
        raise HTTPException(status_code=404, detail=f"CVR-nummer {cvr_nummer} ikke fundet")
    return data[cvr_nummer]


@app.post("/cvr", status_code=201)
def opret_virksomhed(cvr_nummer: str, virksomhed: Virksomhed):
    data = load_data()
    if cvr_nummer in data:
        raise HTTPException(status_code=409, detail=f"CVR-nummer {cvr_nummer} eksisterer allerede")
    data[cvr_nummer] = virksomhed.model_dump()
    save_data(data)
    return {cvr_nummer: data[cvr_nummer]}


@app.delete("/cvr/{cvr_nummer}", status_code=200)
def slet_virksomhed(cvr_nummer: str):
    data = load_data()
    if cvr_nummer not in data:
        raise HTTPException(status_code=404, detail=f"CVR-nummer {cvr_nummer} ikke fundet")
    slettet = data.pop(cvr_nummer)
    save_data(data)
    return {"slettet": cvr_nummer, "virksomhed": slettet}
