prompt = f"""
You are an expert teacher.

Generate a WELL-FORMATTED lesson note in MARKDOWN.

Details:
- Subject: {data.subject}
- Topic: {data.topic}
- Class: {data.grade}
- Curriculum: {data.curriculum}

FORMAT STRICTLY AS FOLLOWS:

## Lesson Title
## Learning Objectives
(use bullet points)

## Introduction
(short and engaging)

## Main Content
(use subheadings and bullet points where appropriate)

## Worked Examples
(numbered examples)

## Class Activities
(bulleted or numbered)

## Evaluation / Assessment
(at least 5 questions)

## Summary
(short recap)

Use clear headings, bullet points, and spacing.
Do NOT write everything in one paragraph.
"""


    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=800
    )

    return {
    "subject": data.subject,
    "topic": data.topic,
    "grade": data.grade,
    "curriculum": data.curriculum,
    "format": "markdown",
    "lesson_note": response.choices[0].message.content
}


