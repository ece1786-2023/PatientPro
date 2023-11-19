from openai import OpenAI
from log_helper import Mode, log
import os
API_KEY = os.environ.get('OPENAI_API_KEY_PATIENTPRO')
client = OpenAI(api_key=API_KEY)

def call_openai_chat(msgs, mode=Mode.PROD):
    log(mode, 
        "[info] calling openAI chat endpoint",
        f"[debug] calling openAI chat endpoint with:\nmessages={msgs}")
    response = client.chat.completions.create(
        model="gpt-4",
        messages=msgs,
        temperature=1
    )
    log(mode, "successufully called openAI")
    return response.choices[0].message.content