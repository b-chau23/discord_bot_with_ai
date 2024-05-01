import os
import anthropic
import base64
import httpx
from dotenv import load_dotenv

LOG_PATH = "claude_logs.txt"

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_KEY'))

def get_text(model_id, text):
    message = client.messages.create(
        model=model_id,
        max_tokens=1024,
        messages=[
            {"role": "user", "content": text}
        ]
    )
    write_claude_log(message.content[0].text)
    return message.content[0].text

def get_image(model_id, text, image):
    # default message if no instruction provided
    if not text:
        text = "Describe this image."

    if isinstance(image, str):
        image_url = image
        image_media_type = "image/png"
        image_data = base64.b64encode(httpx.get(image_url).content).decode("utf-8")


    message = client.messages.create(
        model=model_id,
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": image_media_type,
                            "data": image_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": text
                    }
                ],
            }
        ],
    )
    write_claude_log(message.content[0].text)
    return message.content[0].text

def write_claude_log(text):
     with open(LOG_PATH, "a") as file:
        file.write("------START------\n")
        file.write(text)
        file.write("\n-------END-------\n")