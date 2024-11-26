import os
HF_TOKEN = os.environ['HFTOKEN']
from huggingface_hub import InferenceClient
client = InferenceClient(api_key=HF_TOKEN)

def qwen_reply(temperature=0.5,max_tokens=1024, top_p=0.7, messages=None):
    if(messages is None):
        return "No input received"
    response = ""
    
    for message in  client.chat.completions.create(
        model="Qwen/Qwen2.5-72B-Instruct",
	temperature=temperature,
	max_tokens=max_tokens,
	top_p=top_p,
	stream=True,
        messages=messages,
    ):
        token = message.choices[0].delta.content
        
        response += token

    return response
