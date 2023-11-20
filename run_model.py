import argparse
import os
from log_helper import Mode, log
import json
from openai_helper import call_openai_chat
import argparse
from metrics import CENTOR

def extract_data(metric, input_record, n_shots=0, example_records=[], example_outputs=[]):
    if n_shots != len(example_records) or n_shots != len(example_outputs):
        print("[ERROR] n_shots must equal the number of training examples")
        return
    
    messages=[{"role": "system", "content": metric.prompt}]

    if n_shots <= 3:
        for i in range(n_shots):
            messages.extend([
                {"role": "user", "content": example_records[i]},
                {"role": "system", "content": example_outputs[i]}
            ])
    else:
        print("[ERROR] n_shots must be between 0 and 3. This program only supports up to 3-shot learning")
        return
    
    messages.append({"role": "user", "content": input_record})

    response = call_openai_chat(msgs=messages, temp=0)

    return response


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--n_shots', type=int, required=True, help='number of training examples in the prompt')
    parser.add_argument('--output_mode', type=str, required=True, help='output modes: d:data, s:score')
    parser.add_argument('--input_record', type=str, required=True, help='file path to input record')
    parser.add_argument('--metric', type=str, required=True, help='desired metric to create datatable')

    args = parser.parse_args()

    # error check 
    n_shots = args.n_shots
    if n_shots < 0:
        print("[ERROR] n_shots must be positive")

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
    
    metric_str = args.metric
    match metric_str:
        case "CENTOR":
            metric = CENTOR()
        case _:
            print("[ERROR] invalid metric")
            return
        
    # now extract data and call GPT-4
    response = extract_data(metric=metric, input_record=input_record, n_shots=n_shots)
    if not response:
        return
    
    response_json = json.loads(response)
    score = metric.compute_score(response_json)

    if output_mode == 'd':
        print(f"extracted data:\n{response}")
    elif output_mode == 's':
        print(f"{metric.name}: {score}")
    elif output_mode == 'ds':
        print(f"extracted data:\n{response}")
        print(f"\n{metric.name}: {score}")

    


if __name__ == "__main__":
    main()