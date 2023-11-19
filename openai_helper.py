from openai import OpenAI
from log_helper import Mode, log
import os
API_KEY = os.environ.get('OPENAI_API_KEY_PATIENTPRO')
client = OpenAI(api_key=API_KEY)

def call_openai_chat(msgs, mode=Mode.PROD):
    log(mode, 
        "calling openAI chat endpoint",
        f"calling openAI chat endpoint with:\n\nmessages={msgs}")
    response = client.chat.completions.create(
        model="gpt-4",
        messages=msgs,
        temperature=1
    )
    log(mode,
        "successufully called openAI",
        f"successufully called openAI\n\nresponse={response}")
    return response.choices[0].message.content