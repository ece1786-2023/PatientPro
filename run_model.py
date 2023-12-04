import argparse
import os
import json
import sys
import metrics 
from helper.openai_helper import call_openai_chat
from helper.log_helper import Mode, log
from helper.io_helper import read_file_list

def extract_data(metric, input_record, n_shots=0, example_records=[], example_outputs=[]):
    if n_shots != len(example_records) or n_shots != len(example_outputs):
        print("[ERROR] n_shots must equal the number of training examples")
        return
    
    messages=[{"role": "system", "content": metric.prompt}]

    for i in range(n_shots):
        messages.extend([
            {"role": "user", "content": example_records[i]},
            {"role": "system", "content": example_outputs[i]}
        ])
     
    messages.append({"role": "user", "content": input_record})

    response = call_openai_chat(msgs=messages, temp=0)

    return response

def arg_error_check(args):
    o_modes = {'s', 'd', 'ds'}
    metric_list = [c.id for c in metrics.Metric.__subclasses__()]
    if args.n_shots < 0:
        print("[ERROR] n_shots must be positive")
        sys.exit()
    elif not args.output_mode in o_modes:
        print(f"[ERROR] invalid output mode: {args.output_mode}. Please select one of the follwing: {o_modes}")
        sys.exit()
    elif not os.path.exists(args.input_record):
        print(f"[ERROR] File not found: {args.input_record}")
        sys.exit()
    elif not args.metric in metric_list:
        print(f"[ERROR] invalid metric: {args.metric}. Please select one of the following: {metric_list}")
        sys.exit()
    return

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--n_shots', type=int, required=True, help='number of training examples in the prompt')
    parser.add_argument('--output_mode', type=str, required=True, help='output modes: d:data, s:score')
    parser.add_argument('--input_record', type=str, required=True, help='file path to input record')
    parser.add_argument('--metric', type=str, required=True, help='desired metric to create datatable')

    args = parser.parse_args()
    arg_error_check(args)

    n_shots = args.n_shots
    output_mode = args.output_mode
    input_record_path = args.input_record
    input_record = read_file_list([input_record_path])
    metric_str = args.metric
    metric = metrics.get_metric(metric_str)

    # now extract data and call GPT-4
    response = extract_data(metric=metric, input_record=input_record[0], n_shots=n_shots)
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