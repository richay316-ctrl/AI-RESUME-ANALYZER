from fastapi import FastAPI
from pydantic import BaseModel

from database import (
    create_table,
    save_analysis,
    get_analysis
)


app = FastAPI(
    title="Resume Job Match Backend"
)


# Database table create
create_table()



# Data format
class ResumeData(BaseModel):

    resume_name: str
    job_description: str
    score: float
    skills: list
    missing_keywords: list



# Home API
@app.get("/")
def home():

    return {
        "message": "Resume Match Backend Running"
    }



# Save result API
@app.post("/save-analysis")
def save_resume_analysis(data: ResumeData):

    save_analysis(
        data.resume_name,
        data.job_description,
        data.score,
        data.skills,
        data.missing_keywords
    )

    return {
        "message": "Analysis saved successfully"
    }



# Get all records API
@app.get("/results")
def get_results():

    data = get_analysis()

    return {
        "results": data
    }