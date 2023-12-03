import os
from openai import OpenAI
from helper.log_helper import Mode, log

API_KEY = os.environ.get('OPENAI_API_KEY_PATIENTPRO')
client = OpenAI(api_key=API_KEY)

def call_openai_chat(msgs, temp=1, mode=Mode.PROD):
    log(mode, 
        "Calling OpenAI chat endpoint",
        f"Calling OpenAI chat endpoint with:\n\nmessages = {msgs}")
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=msgs,
        temperature=temp,
    )
    log(mode,
        "Successfully called OpenAI",
        f"Successfully called OpenAI\n\nresponse = {response}")
    return response.choices[0].message.content