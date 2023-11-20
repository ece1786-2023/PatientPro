from openai_helper import call_openai_chat
import argparse
import os
from log_helper import Mode, log

def read_seed_records(file_paths):
    records = []
    for path in file_paths:
        if os.path.exists(path):
            with open(path, 'r') as file:
                records.append(file.read())
        else:
            print(f"[ERROR] File not found: {path}")
    return records


def save_records_to_file(records, dir):
    # Create the dir if it doesn't exist
    if not os.path.exists(dir):
        os.makedirs(dir)

    #save each record to a file
    record_id = 0
    for record in records:
        if record == "":
            print("[WARN] empty output generated. Ommitted from results")
            continue
        fname = f"sr_{record_id}.txt"
        path = os.path.join(dir, fname)

        with open(path, 'w') as file:
            file.write(record)
        
        #TODO: find a better way to id records.
        record_id += 1

def synthesize_records_centor(seed_records, new_record_count, output_dir):
    #check token limits:
    n_seed_records = len(seed_records)
    if (n_seed_records + new_record_count) > 16:
        print(len(seed_records))
        print(new_record_count)
        print("[ERROR] total token count will exceed token limit of model. Reduce number of seed records or lower number of output records.")
        return None
    
    system_prompt = f"synthea creates synthetic but realistic EHR patient records. Given {n_seed_records} example{'' if n_seed_records == 1 else 's'} of such record create {new_record_count + n_seed_records} example{'' if new_record_count == 1 else 's'} with different data but a similar chief complaint.\n\nMake sure to vary the following data:\n\n1. age\n2. temp\n3. tonsils condition\n4. lymph nodes condition\n5. cough presence\End each record by the following string:\n####"

    messages=[{"role": "system", "content": system_prompt}]

    for record in seed_records:
        if record == "":
            print("[WARN] empty seed record. Ommitted from input")
            continue
        messages.append(
            {"role": "user", "content": record}
        )

    response = call_openai_chat(msgs=messages, mode=Mode.DEBUG)
    
    output_records = response.split("####")
    save_records_to_file(output_records, output_dir)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--n_new_records', type=int, required=True, help='Number of new records to generate')
    parser.add_argument('--output_dir', type=str, required=True, help='Name of the output directory for new synthetic records')
    parser.add_argument('--seed_records', type=str, required=True, help='Comma separated list of seed record file paths')

    args = parser.parse_args()

    output_dir = args.output_dir
    n_new_records = args.n_new_records

    seed_records_paths = args.seed_records.split(',')
    seed_records = read_seed_records(seed_records_paths)

    synthesize_records_centor(seed_records=seed_records, new_record_count=n_new_records, output_dir=output_dir)
    

if __name__ == "__main__":
    main()












