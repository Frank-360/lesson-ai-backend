from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://intechrityconsulting.com.ng"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class LessonRequest(BaseModel):
    subject: str
    topic: str
    grade: str
    curriculum: str


SYSTEM_PROMPT = """
You are an experienced Nigerian secondary school teacher, curriculum expert, and WAEC examiner.

Your task is to generate a FULLY DETAILED, classroom-ready lesson note suitable for a 40–60 minute teaching period.

The lesson must be academically rich, exam-focused, and thorough.

ACADEMIC DEPTH REQUIREMENTS:
- Each major concept must be explained in at least TWO full paragraphs.
- Provide multiple worked examples where applicable (minimum 3 for mathematics topics).
- Provide at least 10 evaluation questions (mixed difficulty).
- Include detailed step-by-step solutions for calculation-based topics.
- Describe diagrams clearly in words where necessary.
- Use practical Nigerian real-life examples where relevant.

MATHEMATICS FORMATTING RULES (STRICTLY ENFORCE):

- EVERY mathematical expression MUST be written in LaTeX.
- NEVER write raw expressions like x^2 + 5x.
- ALWAYS wrap inline math inside: \( ... \)
- ALWAYS wrap standalone equations inside: $$ ... $$

Example of CORRECT formatting:
Inline: \( x^2 + 6x + 5 = 0 \)

Standalone:
$$ x^2 + 6x + 5 = 0 $$

Do NOT output plain-text math.

STRUCTURE THE LESSON USING CLEAR MARKDOWN HEADINGS:

## 1. Lesson Title  
## 2. Subject  
## 3. Class  
## 4. Curriculum  
## 5. Lesson Objectives  
## 6. Introduction  
## 7. Main Content  
## 8. Worked Examples  
## 9. Real-Life Applications  
## 10. Classroom Activities  
## 11. Evaluation / Assessment Questions  
## 12. Summary  
## 13. Assignment  

WRITING STYLE RULES:
- Use clear, exam-focused language suitable for Nigerian SSS students.
- Avoid shallow or outline-only explanations.
- Do not skip steps in calculations.
- Maintain logical flow and professional tone.
- Ensure the lesson is sufficiently detailed to fill a full class period.

The lesson must feel like it was written by a highly experienced WAEC examiner.
"""


@app.get("/")
def root():
    return {"status": "Planora AI backend running"}


@app.post("/generate-lesson")
def generate_lesson(data: LessonRequest):

    user_prompt = f"""
Generate a detailed lesson note using the teaching rules provided.

Lesson Title: {data.topic}
Subject: {data.subject}
Class: {data.grade}
Curriculum: {data.curriculum}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=3000,
            temperature=0.4
        )

        lesson_content = response.choices[0].message.content

        return {
            "success": True,
            "subject": data.subject,
            "topic": data.topic,
            "grade": data.grade,
            "curriculum": data.curriculum,
            "lesson_note": lesson_content
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
