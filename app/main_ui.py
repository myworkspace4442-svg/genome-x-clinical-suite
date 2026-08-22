from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

# Core Engine အဟောင်းများ သို့မဟုတ် ML Engine များကို Import လုပ်ပါ
from app.engine.core_engine import GenomeXEngine  # cite: image_d0b01e.png
from explainability.shap_engine import SHAPExplainerEngine  # cite: image_d10e58.png

app = FastAPI(title="Genome-X Suite API", version="1.0")

# Frontend (Vite Port 5173 / 5174) မှ လာသော Request များကို ခွင့်ပြုရန် CORS Config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SequenceRequest(BaseModel):
    sequence: str
    pathogen: str = "E. coli"
    antibiotic: str = "Ciprofloxacin"


@app.get("/")
def read_root():
    return {"status": "Active", "engine": "Genome-X Core v1.0"}


@app.post("/api/v1/predict-amr")
def predict_amr(payload: SequenceRequest):
    try:
        # 1. Pipeline/Engine မှ Real Prediction ရယူခြင်း
        # (စမ်းသပ်ရန် Sample Logic - မိမိ Model Logic နှင့် ပြန်ပြင်နိုင်ပါသည်)
        return {
            "predicted_phenotype": "RESISTANT",
            "confidence": 95.4,
            "primary_target": "gyrA_S83L",
            "secondary_target": "parC_S80I",
            "shap_features": [
                {"gene": "gyrA (S83L Mutation)", "value": 0.48,
                                "impact": "High Resistance Driver"},
                {"gene": "parC (S80I Mutation)", "value": 0.32,
                 "impact": "Secondary Hotspot"},
                {"gene": "qnrS1 (Plasmid Gene)", "value": 0.12,
                 "impact": "Moderate Resistance Effect"},
                {"gene": "acrB (Efflux Pump)", "value": 0.08,
                 "impact": "Minor Contribution"}
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
