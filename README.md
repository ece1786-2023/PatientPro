# PatientPro

## Setup
1. clone repo
2. install requirements:
```
pip install -r requirements.txt
```
3. configure api key from openAI:
    - setup an API key as per openAI docs
    - export it to an env var as follows:
    ```
    export export OPENAI_API_KEY_PATIENTPRO=<INSERT API KEY HERE>
    ```
4. (optional) you can also add the line in step 3 to your `~/.bashrc` or `~/.zshrc` to presist it.

5. you're good to go!

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


## CENTOR score
the script `centor.py` can extract the data needed to compute the CENTOR score and/or compute the score directly. 

you can use the script by providing the following parameters:
- `n_shots`: the number of training "shots" (examples) supplied in the context. note that this is currently limited to a maximum of 3 examples.
- `output_mode`: one of 3 output modes:
  - `'d'`: data -- shows the extracted relevant data only
  - `'s'`: score -- shows the computed CENTOR based on the data
  - `'ds'`: data+score -- shows the extracted data and the computed CENTOR score
- `input_record` the file paths to the input record on which the extraction/computation will be done.

example usage:
```
centor.py --n_shots 0 --output_mode d --input_record record_0.txt
```