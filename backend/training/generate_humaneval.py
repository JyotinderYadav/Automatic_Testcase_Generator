import os
import json
import gzip
import urllib.request
import random

def download_humaneval():
    url = "https://github.com/openai/human-eval/raw/master/data/HumanEval.jsonl.gz"
    output_path = "HumanEval.jsonl.gz"
    if not os.path.exists(output_path):
        print("Downloading HumanEval dataset...")
        urllib.request.urlretrieve(url, output_path)
    return output_path

def create_dataset():
    gz_path = download_humaneval()
    
    records = []
    with gzip.open(gz_path, "rt") as f:
        for line in f:
            data = json.loads(line)
            
            # The prompt includes the function signature and docstring
            # canonical_solution has the working implementation
            # test has the test cases
            
            prompt_str = data["prompt"] + data["canonical_solution"]
            test_code = data["test"]
            
            system_prompt = "You are a Senior Software Test Engineer & AI Test Generator. Output ONLY a valid JSON object with keys: test_cases_table, edge_cases, executable_code, bug_risk. Do NOT include any extra text."
            
            user_prompt = f"INPUT TYPE: Code snippet\\nDATA: {prompt_str}\\nFramework: pytest\\nMode: balanced"
            
            # Synthesize the rest of the JSON structure so it matches our application's expected format
            assistant_response = {
                "test_cases_table": "| Test Case Name | Input | Expected Output | Type |\\n|---|---|---|---|\\n| Standard Execution | Valid Inputs | Expected Result | Positive |\\n| Boundary Conditions | Edge Inputs | Handled | Edge |",
                "edge_cases": "- Empty inputs\\n- Invalid data types\\n- Extremes and bounds",
                "executable_code": test_code,
                "bug_risk": "- Unhandled exceptions\\n- Performance scaling issues with large inputs\\n- Edge case mishandling"
            }
            
            chat_record = {
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                    {"role": "assistant", "content": json.dumps(assistant_response)}
                ]
            }
            records.append(chat_record)
    
    # Shuffle for good distribution
    random.seed(42)
    random.shuffle(records)
    
    # 90% train, 10% valid
    split_idx = int(len(records) * 0.9)
    train_records = records[:split_idx]
    valid_records = records[split_idx:]
    
    with open("train.jsonl", "w") as f_train:
        for r in train_records:
            print(json.dumps(r), file=f_train)
            
    with open("valid.jsonl", "w") as f_valid:
        for r in valid_records:
            print(json.dumps(r), file=f_valid)
            
    print(f"Generated train.jsonl ({len(train_records)} examples) and valid.jsonl ({len(valid_records)} examples) from HumanEval.")

if __name__ == "__main__":
    create_dataset()
