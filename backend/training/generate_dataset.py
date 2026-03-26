import json
import random

def generate_dataset():
    # Synthetic examples of test generation
    examples = [
        {
            "system": "You are a Senior Software Test Engineer & AI Test Generator. Output ONLY a valid JSON object with keys: test_cases_table, edge_cases, executable_code, bug_risk. Do NOT include any extra text.",
            "user": "INPUT TYPE: API\\nDATA: POST /api/login Request: {\"email\": \"string\", \"password\": \"string\"}\\nFramework: pytest\\nMode: balanced",
            "assistant": {
                "test_cases_table": "| Test Case | Input | Expected | Type |\\n|---|---|---|---|\\n| Valid Login | email: user@test.com | 200 OK | Positive |\\n| Invalid Password | email: user@test.com | 401 | Negative |",
                "edge_cases": "- Empty email\\n- Very long password",
                "executable_code": "def test_login():\\n    assert True",
                "bug_risk": "- Rate limiting\\n- SQL injection"
            }
        },
        {
            "system": "You are a Senior Software Test Engineer & AI Test Generator. Output ONLY a valid JSON object with keys: test_cases_table, edge_cases, executable_code, bug_risk. Do NOT include any extra text.",
            "user": "INPUT TYPE: User Story\\nDATA: As a user, I want to add items to my cart so that I can checkout.\\nFramework: jest\\nMode: balanced",
            "assistant": {
                "test_cases_table": "| Test Case | Input | Expected | Type |\\n|---|---|---|---|\\n| Add valid item | item_id: 1 | Item added to cart | Positive |\\n| Add out of stock | item_id: 2 | Error | Negative |",
                "edge_cases": "- Cart limit exceeded",
                "executable_code": "test('add item', () => { expect(true).toBe(true); });",
                "bug_risk": "- Race condition when decrementing stock"
            }
        }
    ]

    # Duplicate to create a minimal dataset
    dataset = examples * 10
    
    with open("train.jsonl", "w") as f_train, open("valid.jsonl", "w") as f_valid:
        for i, example in enumerate(dataset):
            record = {
                "messages": [
                    {"role": "system", "content": example["system"]},
                    {"role": "user", "content": example["user"]},
                    {"role": "assistant", "content": json.dumps(example["assistant"])}
                ]
            }
            line = json.dumps(record) + "\n"
            if i % 5 == 0:
                f_valid.write(line)
            else:
                f_train.write(line)

    print(f"Generated train.jsonl and valid.jsonl with {len(dataset)} synthetic examples.")

if __name__ == "__main__":
    generate_dataset()
