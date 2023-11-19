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
            print(f"ERROR: File not found: {path}")
    return records


def save_records_to_file(records, dir):
    # Create the dir if it doesn't exist
    if not os.path.exists(dir):
        os.makedirs(dir)

    #save each record to a file
    for i, record in enumerate(records):
        fname = f"sr_{i}.txt"
        path = os.path.join(dir, fname)

        with open(path, 'w') as file:
            file.write(record)

def synthesize_records_centor(seed_records, new_record_count, output_dir):
    #check token limits:
    if (len(seed_records) + new_record_count) > 16:
        print(len(seed_records))
        print(new_record_count)
        print("ERROR: total token count will exceed token limit of model. Reduce number of seed records or lower number of output records.")
        return None
    
    system_prompt = f"synthea creates synthetic but realistic EHR patient records. Given an example of such record create {new_record_count} other examples with different data but a similar chief complaint.\n\nMake sure to vary the following data:\n\n1. age\n2. temp\n3. tonsils condition\n4. lymph nodes condition\n5. cough presence\nSeparate records by the following string: ####"

    messages=[{"role": "system", "content": system_prompt}]

    for record in seed_records:
        messages.append(
            {"role": "user", "content": record}
        )

    response = call_openai_chat(msgs=messages, mode=Mode.DEV)
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











