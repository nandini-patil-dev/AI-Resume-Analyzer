

import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()


def generate_resume_feedback(resume_text, job_description):

    print("STEP 1: Checking API key...")

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError("Gemini API key is missing.")

    print("STEP 2: Connecting to Gemini...")

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.8-flash",
        google_api_key=api_key,
        temperature=0.3,
        max_retries=1
    )

    prompt = ChatPromptTemplate.from_template("""
    You are an experienced technical recruiter.

    Analyze this resume against the job description.

    RESUME:
    {resume}

    JOB DESCRIPTION:
    {job_description}

    Provide:
    1. Resume Summary
    2. Relevant Skills
    3. Missing Skills
    4. Resume Improvement Suggestions
    5. Recommended Learning Areas

    Never invent qualifications or experience.
    """)

    chain = prompt | llm

    print("STEP 3: Sending request to Gemini...")

    response = chain.invoke({
        "resume": resume_text,
        "job_description": job_description
    })

    print("STEP 4: Gemini response received!")

    return response.content
