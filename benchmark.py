import metrics
from io_helper import read_file_list, get_dir_files
import argparse
import run_model
import sys
import os
import json
import pandas as pd



def benchmark(metric, input_dir_str, n_shots=0):
    files = get_dir_files(input_dir_str)
    jsons = []
    scores = []
    
    for f in files:
        print(f'now analyzing {f}')
        ehr = ""
        with open(f, 'r') as file:
            ehr = file.read()
        jsonski = json.loads(run_model.extract_data(metric, ehr, n_shots))
        jsons.append(jsonski)
        scores.append(metric.compute_score(jsonski))
    df = pd.DataFrame(jsons)
    df.insert(0, 'EHR', files)
    
    df['Score'] = scores

    return df


def arg_error_check(args):
    metrics = {"centor", "qsofa"}
    if args.n_shots < 0 or args.n_shots > 3:
        print("[ERROR] n_shots must be an integer between 0 and 3.")
        sys.exit()
    elif not os.path.exists(args.input_dir):
        print(f"[ERROR] Directory not found: {args.input_dir}")
        sys.exit()
    elif not args.metric in metrics:
        print(f"[ERROR] invalid metric: {args.metric}. Please select one of the following: {metrics}")
        sys.exit()
    return

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--n_shots', type=int, required=True, help='number of training examples in the prompt')
    parser.add_argument('--input_dir', type=str, required=True, help='Directory of samples')
    parser.add_argument('--metric', type=str, required=True, help='desired metric to create datatable')

    args = parser.parse_args()
    arg_error_check(args)

    n_shots = args.n_shots
    metric_str = args.metric
    input_dir_str = args.input_dir
    metric = metrics.get_metric(metric_str)
    
    df = benchmark(metric, input_dir_str, n_shots)

    print(df)
    print(df.to_latex())
        

if __name__ == "__main__":
    main()


