import os
import base64
import httpx
from openai import OpenAI
from dotenv import load_dotenv

LOG_PATH = "gpt_logs.txt"

load_dotenv()
client = OpenAI(api_key=os.getenv('API_KEY'))

def get_text(model_id, text):
    response = client.chat.completions.create(
        model=model_id,
        messages=
        [
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": text}
        ]
    )
    write_gpt_log(response.choices[0].message.content)
    return response.choices[0].message.content

def get_image(url, text):
    # defualt prompt if no additional instructions have been passed
    if not text:
        text = "What is in this image?"
    
    image_url = url
    image_media_type = "image/png"
    image_data = base64.b64encode(httpx.get(image_url).content).decode("utf-8")


    response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {
        "role": "user",
        "content": [
            {"type": "text", "text": text},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:{image_media_type};base64,{image_data}",
                },
            },
        ],
        }
    ],
    max_tokens=500,
    )
    write_gpt_log(response.choices[0].message.content)
    return response.choices[0].message.content

def create(text):
    # Do not call API if there is no prompt (am poor, need to save money)
    if not text:
        return "Invalid Prompt"
    
    response = client.images.generate(
        model="dall-e-3",
        prompt=text,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    return response.data[0].url

def write_gpt_log(text):
     with open(LOG_PATH, "a") as file:
        file.write("------START------\n")
        file.write(text)
        file.write("\n-------END-------\n")