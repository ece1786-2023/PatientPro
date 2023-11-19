from openai_helper import call_openai_chat
import argparse
import os
from log_helper import Mode, log
import json

def extract_data(input_record, n_shots=0, example_records=[], example_outputs=[]):
    if n_shots != len(example_records) or n_shots != len(example_outputs):
        print("[ERROR] n_shots must equal the number of training examples")
        return
    
    output_schema = "{\n  \"age\": int,\n  \"tonsil_swelling\": boolean,\n  \"lymph_swelling\": boolean,\n  \"temp\": float,\n  \"cough_present\": boolean\n}"
    centor_extraction_prompt = f"given a medical record of a patient, extract the following pieces of information:\n\n1. age (integer)\n2. temperature in Celsius (float)\n3. exudate or swollen tonsils (boolean True/False)\n4. tender/swollen anterior cervical lymph nodes (boolean)\n5. cough present (boolean)\n\nuse the following schema for the output:\n\n{output_schema}"
    messages=[{"role": "system", "content": centor_extraction_prompt}]

    if n_shots == 0:
        pass
    elif n_shots == 1:
        messages.extend([
            {"role": "user", "content": example_records[0]},
            {"role": "system", "content": example_outputs[0]}
        ])
    elif n_shots == 2:
        messages.extend([
            {"role": "user", "content": example_records[0]},
            {"role": "system", "content": example_outputs[0]},
            {"role": "user", "content": example_records[1]},
            {"role": "system", "content": example_outputs[1]},
        ])
    elif n_shots == 3:
        messages.extend([
            {"role": "user", "content": example_records[0]},
            {"role": "system", "content": example_outputs[0]},
            {"role": "user", "content": example_records[1]},
            {"role": "system", "content": example_outputs[1]},
            {"role": "user", "content": example_records[2]},
            {"role": "system", "content": example_outputs[2]}
        ])
    else:
        print("[ERROR] n_shots must between 0 and 3. This program only supports up to 3-shot learning")
        return
    
    messages.append({"role": "user", "content": input_record})

    response = call_openai_chat(msgs=messages, temp=0)

    return response


def compute_centor_score(data):
    score = 0

    if 3 <= data['age'] <= 14:
        score += 1
    elif data['age'] >= 45:
        score -= 1
    
    if data['tonsil_swelling']:
        score += 1
    
    if data['lymph_swelling']:
        score += 1
    
    if data['temp'] > 38.0:
        score += 1
    
    if data['cough_present']:
        score += 1
    
    return score


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--n_shots', type=int, required=True, help='number of training examples in the prompt')
    parser.add_argument('--output_mode', type=str, required=True, help='output modes: d:data, s:score')
    parser.add_argument('--input_record', type=str, required=True, help='file path to input record')

    args = parser.parse_args()

    n_shots = args.n_shots
    
    output_mode = args.output_mode
    if not output_mode in {'s', 'd', 'ds'}:
        print("[ERROR] output mode not recognized. Please select one of the follwing: d, s, or ds")
    
    input_record_path = args.input_record
    input_record = None
    if os.path.exists(input_record_path):
            with open(input_record_path, 'r') as file:
                input_record = file.read()
    else:
        print(f"[ERROR] File not found: {input_record_path}")
        return

    response = extract_data(input_record=input_record, n_shots=n_shots)
    if not response:
        return
    response_json = json.loads(response)
    centor_score = compute_centor_score(response_json)

    if output_mode == 'd':
        print(f"extracted data:\n{response}")
    elif output_mode == 's':
        print(f"CENTOR score: {centor_score}")
    elif output_mode == 'ds':
        print(f"extracted data:\n{response}")
        print(f"\nCENTOR score: {centor_score}")
    
    
    
if __name__ == "__main__":
    main()