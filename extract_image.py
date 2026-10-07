import os
from groq import Groq
from dotenv import load_dotenv
import streamlit as st
import json
import requests

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key)


def extract_image_details(story: str, child_name: str, characters: list, setting: str):
   

    prompt = f"""
    Analyze this children's story and prepare information for an
    image-generation model.

    STORY:
    {story}

    ORIGINAL CHARACTER INPUT:
    {characters}

    ORIGINAL SETTING:
    {setting}

    MAIN CHILD:
    {child_name}

    Extract the visual information needed for an illustration.

    Return ONLY valid JSON in this exact format:

    {{
        "characters": [
            {{
                "name": "character name",
                "appearance": "important visual characteristics"
            }}
        ],
        "scene": "specific location and background",
        "action": "what the characters are doing",
        "objects": ["important object 1", "important object 2"],
        "mood": "emotional atmosphere"
    }}

    Rules:

    1. Include only characters that are actually present in the story.
    2. Do not invent new characters.
    3. Include the main child character.
    4. Preserve physical characteristics mentioned in the story.
    5. Do not invent unnecessary physical characteristics.
    6. Describe only what should be visible in the illustration.
    7. Keep the description concise.
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        reasoning_effort="low",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    details = response.choices[0].message.content

    print("RAW IMAGE DETAILS:")
    print(details)

    try:
        return json.loads(details)
    except json.JSONDecodeError:
        print("Could not parse image details:")
        print(details)
        return None