from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

class LessonRequest(BaseModel):
    subject: str
    topic: str
    grade: str
    curriculum: str = "Nigerian"

@app.post("/generate-lesson")
async def generate_lesson(data: LessonRequest):
    prompt = f"""
You are an expert teacher.

Generate a detailed lesson note for:
Subject: {data.subject}
Topic: {data.topic}
Class: {data.grade}
Curriculum: {data.curriculum}

Include:
- Lesson objectives
- Introduction
- Main content
- Examples
- Class activities
- Evaluation questions
- Summary
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800
    )

    return {
        "lesson_note": response.choices[0].message.content
    }
