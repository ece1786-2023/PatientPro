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
- `metric`: The desired metric for which the corresponding datatable will be tailored. Note that as of 2023-11-20, the only metric available is CENTOR score.
- `n_shots`: The number of training "shots" (examples) supplied in the context (currently limited to a maximum of 3).
- `output_mode`: One of 3 output modes:
  - `'d'`: Data -- shows the extracted relevant data only
  - `'s'`: Score -- shows the computed metric score based on the data
  - `'ds'`: Data+Score -- shows both the extracted data and the computed score
- `input_record`: the file path to the input EHR on which the extraction/computation will be done.

example usage:
```
run_model.py --metric=CENTOR --n_shots 0 --output_mode d --input_record record_0.txt
```


## Synthetic Record Generation
in order to train and test our data extraction and score computation logic we need examples of medical records.
considering the difficulty of accessing records that match our needed usecase we have come up with a method of synthetically creating records for a specific usecase
the script `generate_record.py` can generate a number of synthetic records given a seed input of one or more records.

you can use the script by providing the following parameters:
- `n_new_records`: the number of new records to generate
- `output_dir`: the output directory to save the generated records to
- `seed_records` a comma separated list of file paths to the records used as a seed for the generation

example usage:
```
python generate_record.py --n_new_records 2 --output_dir synthetic_records --seed_records=sample_1.txt
```

**NOTE:** the generation script is currently tailored towards records relevant to CENTOR score calculation and will be generalized in the future.


