import os
import json
import gzip
import urllib.request
import random
from datasets import load_dataset

def download_humaneval():
    url = "https://github.com/openai/human-eval/raw/master/data/HumanEval.jsonl.gz"
    output_path = "HumanEval.jsonl.gz"
    if not os.path.exists(output_path):
        print("Downloading HumanEval dataset...")
        urllib.request.urlretrieve(url, output_path)
    return output_path

def get_humaneval_records():
    print("Downloading EvalPlus HumanEval dataset...")
    ds = load_dataset("evalplus/humanevalplus")
    records = []
    for split in ds.keys():
        for row in ds[split]:
            prompt_str = row["prompt"] + row.get("canonical_solution", "")
            test_code = row["test"]
            records.append((prompt_str, test_code))
    return records

def get_mbpp_records():
    print("Downloading EvalPlus MBPP dataset...")
    # Load dataset using Hugging Face datasets
    ds = load_dataset("evalplus/mbppplus")
    
    records = []
    # Use the train and test splits if available
    splits = ds.keys()
    for split in splits:
        for row in ds[split]:
            prompt_str = row.get("text", "") + "\\n" + row.get("code", "")
            
            # test_list is usually a list of strings
            test_list = row.get("test_list", [])
            test_setup = row.get("test_setup_code", "")
            
            # Combine the test assertions into a single code block
            test_code = test_setup + "\\n" + "\\n".join(test_list)
            
            records.append((prompt_str, test_code))
            
    return records

def create_dataset():
    he_records = get_humaneval_records()
    mbpp_records = get_mbpp_records()
    
    all_raw_data = he_records + mbpp_records
    print(f"Total Combined Records: {len(all_raw_data)} (HumanEval: {len(he_records)}, MBPP: {len(mbpp_records)})")
    
    records = []
    system_prompt = "You are a Senior Software Test Engineer & AI Test Generator. Output ONLY a valid JSON object with keys: test_cases_table, edge_cases, executable_code, bug_risk. Do NOT include any extra text."
            
    for prompt_str, test_code in all_raw_data:
        user_prompt = f"INPUT TYPE: Code snippet\\nDATA: {prompt_str}\\nFramework: pytest\\nMode: balanced"
        
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
            
    print(f"Generated train.jsonl ({len(train_records)} examples) and valid.jsonl ({len(valid_records)} examples) from Combined MBPP & HumanEval.")

if __name__ == "__main__":
    create_dataset()
