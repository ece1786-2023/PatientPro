import argparse
import sys
import os
import json
import pandas as pd
import csv
import metrics
import run_model
from helper.io_helper import read_file_list, get_dir_files

def create_template(metric, input_dir_str):
    headers = ["EHR"] + metric.extract_keys() + ["Score"]
    files = get_dir_files(input_dir_str)
    o_fn = metric.id + "_labels.csv"
    with open(o_fn, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows([[file] + [""]*(len(headers)-1) for file in files])
    print('created', o_fn)

def compare(df1, metric):
    labels = 'labels/' + metric.id + "_labels.csv"
    df2 = pd.read_csv(labels)
    # diff = df1.compare(df2)
    diff = df1 == df2
    diffrows = df1.compare(df2)
    return diff, diffrows

def benchmark(metric, input_dir_str, n_shots=0):
    files = get_dir_files(input_dir_str)
    jsons = []
    scores = []
    
    for i in range(len(files)):
        # print(f'now analyzing {f}')
        bar = '#'*(i+1) + '-'*(len(files)-i-1)
        percent_complete = (i+1)/len(files)
        print(f"\rProgress: [{bar}] {percent_complete:.1%}", end='')
        ehr = ""
        with open(files[i], 'r') as file:
            ehr = file.read()
        jsonski = json.loads(run_model.extract_data(metric, ehr, n_shots))
        jsons.append(jsonski)
        scores.append(metric.compute_score(jsonski))
    print()
    df = pd.DataFrame(jsons)
    df.insert(0, 'EHR', files)
    df['Score'] = scores

    return df


def arg_error_check(args):
    metric_list = [c.id for c in metrics.Metric.__subclasses__()]
    if args.n_shots < 0 or args.n_shots > 3:
        print("[ERROR] n_shots must be an integer between 0 and 3.")
        sys.exit()
    elif not os.path.exists(args.input_dir):
        print(f"[ERROR] Directory not found: {args.input_dir}")
        sys.exit()
    elif not args.metric in metric_list:
        print(f"[ERROR] invalid metric: {args.metric}. Please select one of the following: {metric_list}")
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
    
    # create_template(metric, input_dir_str)
    df = benchmark(metric, input_dir_str, n_shots)

    print(f'GPT-4 Results:\n{df}\n')
    diff, diffrows = compare(df, metric)
    # print('Difference between labels and results:\n',diff)
    print(f'Rows different from results:\n{diffrows}\n')
    num_samples = len(get_dir_files(input_dir_str))
    incorr = len(diffrows)
    acc = (num_samples - incorr) / num_samples
    print(f'Accuracy: {acc*100:3f}%')
    # print(df.to_latex())
        

if __name__ == "__main__":
    main()


