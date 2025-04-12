
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pydantic import BaseModel
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

excel_path = "Merged_JoSAA_with_Fees2.xlsx"
sheets = pd.read_excel(excel_path, sheet_name=None)

def clean_sheet(df):
    df = df.copy()
    df["Closing Rank"] = pd.to_numeric(df["Closing Rank"], errors="coerce")
    df = df.dropna(subset=["Closing Rank"])
    return df

class PredictRequest(BaseModel):
    name: str
    rank: int
    seatType: str
    round: str
    gender: str
    state: str

@app.post("/api/predict")
async def predict(data: PredictRequest):
    sheet_name = list(sheets.keys())[int(data.round)-1]
    df = clean_sheet(sheets[sheet_name])

    filtered = df[
        (df["Seat Type"] == data.seatType) &
        (df["Gender"].isin([data.gender, "Gender-Neutral"])) &
        (df["Closing Rank"] >= data.rank)
    ]

    results = filtered[[
        "Institute Name", "Academic Program Name", "Quota", "Seat Type", "Gender",
        "Closing Rank", "Total B.Tech Fees (4 Years)", "Avg. Yearly Fees",
        "Average Package", "Highest Package"
    ]].rename(columns={
        "Total B.Tech Fees (4 Years)": "Total B.Tech Fees"
    }).to_dict(orient="records")

    return results
