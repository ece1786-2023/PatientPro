# PatientPro

## Setup
1. Clone repository
2. Set up virtual environment via `venv`:
    -  Create virtual environment: 
        ```
        python3 -m venv patientpro
        ```
    - Activate virtual environment:
        ```
        source patientpro/bin/activate
        ```
3. Install required dependencies:
    ```
    pip install -r requirements.txt
    ```
4. Configure OpenAI API key:
    - Set up API key as per OpenAI documentation 
    - Export to environment variable as follows:
    ```
    export OPENAI_API_KEY_PATIENTPRO=<INSERT API KEY HERE>
    ```
5. (Optional) Add the line in step 4 to your `~/.bashrc` or `~/.zshrc` to persist it.

5. You're good to go! Happy datatable generation!

## Create a datatable from an EHR
The script `run_model.py` prompts GPT-4 to extract information from a given EHR to create a corresponding datatable tailored to a specified metric, with options to few-shot the prompt and compute the metric score. 

The script requires the following parameters:
- `metric`: The desired metric for which the corresponding datatable will be tailored. Note that as of 2023-11-20, the only metric available is Centor score.
- `n_shots`: The number of training "shots" (examples) supplied in the context (currently limited to a maximum of 3).
- `output_mode`: One of 3 output modes:
  - `'d'`: Data -- shows the extracted relevant data only
  - `'s'`: Score -- shows the computed metric score based on the data
  - `'ds'`: Data+Score -- shows both the extracted data and the computed score
- `input_record`: the file path to the input EHR on which the extraction/computation will be done.

Example usage:
```
python run_model.py --metric centor --n_shots 0 --output_mode d --input_record record_0.txt
```


## Synthetic Record Generation
The script `generate_record.py` prompts GPT-4 to generate a given number of synthetic EHRs given a verified seed record to reduce hallucination. As of 2023-11-28, the PatientPro team has experienced difficulty procuring a dataset of real anonymized freeform text EHRs, and has thus defaulted to synthetic generation of EHRs with medical expert-verified seed records.

The script requires the following parameters:

- `metric`: The desired metric for which the generated EHRs will be tailored. As of 2023-11-28, the only metric available is Centor score.
- `n_new_records`: The number of new records to generate.
- `output_dir`: The output directory where generated records will be saved.
- `seed_records`: A comma-separated list of file paths to the seed records used to assist generation.

Example usage:
```
python generate_record.py --metric centor --n_new_records 2 --output_dir synthetic_records --seed_records seed_records_centor/centor_seed_1.txt
```



