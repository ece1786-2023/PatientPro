from openai import OpenAI
from log_helper import Mode, log
client = OpenAI(api_key='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')

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