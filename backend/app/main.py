import os
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TestRequest(BaseModel):
    input_type: str
    input_data: str
    test_framework: str
    mode: str = "balanced"

class TestResponse(BaseModel):
    test_cases_table: str
    edge_cases: str
    executable_code: str
    bug_risk: str
    success: bool
    error: Optional[str] = None

@app.post("/generate-tests", response_model=TestResponse)
async def generate_tests(request: TestRequest):
    try:
        system_prompt = f"""You are a Senior Software Test Engineer & AI Test Generator.
Analyze the user input and generate comprehensive, structured, and executable test cases for the {request.test_framework} framework.

Output ONLY a valid JSON object with the following keys:
- "test_cases_table": A Markdown table with columns | Test Case Name | Input | Expected Output | Type | (Include Positive, Negative, Edge, and Security).
- "edge_cases": A Markdown list of edge cases considered.
- "executable_code": Clean, runnable code using {request.test_framework} with proper assertions.
- "bug_risk": A Markdown summary of potential failures and vulnerabilities.

Do NOT include any extra text before or after the JSON.
"""

        user_prompt = f"INPUT TYPE: {request.input_type}\nDATA: {request.input_data}\nFramework: {request.test_framework}\nMode: {request.mode}"

        client = OpenAI(
            base_url="http://localhost:8080/v1",
            api_key="mlx-local-no-key-required"
        )

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model="Qwen/Qwen2.5-Coder-1.5B-Instruct",
            temperature=0.2,
            response_format={"type": "json_object"}
        )

        response_text = chat_completion.choices[0].message.content
        parsed = json.loads(response_text)

        return TestResponse(
            test_cases_table=parsed.get("test_cases_table", "Error parsing table"),
            edge_cases=parsed.get("edge_cases", "Error parsing edge cases"),
            executable_code=parsed.get("executable_code", "Error parsing code"),
            bug_risk=parsed.get("bug_risk", "Error parsing bug risks"),
            success=True,
            error=None
        )

    except Exception as e:
        return TestResponse(
            test_cases_table="",
            edge_cases="",
            executable_code="",
            bug_risk="",
            success=False,
            error=str(e)
        )

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
