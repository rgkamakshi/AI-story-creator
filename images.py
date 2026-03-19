from huggingface_hub import InferenceClient
from PIL import Image
from io import BytesIO
import streamlit as st
import os
import fal_client
import requests

os.environ["FAL_KEY"] = st.secrets["FAL_KEY"]

#client = InferenceClient(token=st.secrets['HF_TOKEN'])

def generate_image(story: str, setting :str, child_name: str = None ):

    print(story[10:])
    print(child_name)
    #name_instruction = f"featuring a child named {child_name}" 
    prompt = f"""
    Children's book illustration in watercolor storybook art style, soft lighting, cute and colorful,appropriate for children.
    NOT digital cartoon. NOT glossy. NOT video game art. NOT anime.
    
    IMPORTANT: The illustration MUST include all the characters mentioned in the {story} in the {setting} given in the story.

    The illustartion should be appropriate for children and relevant to the story.
    
    Each human character has exactly two legs, two arms, and correct body proportions.
    Characters are clearly separated and not overlapping below the waist.
    Simple clean floor with no reflections or mirror effects.

    Composition: Close-up warm storybook scene, uncluttered background, 
    soft dreamy edges, protagonist fills 60% of the frame.
    Mood: Warm, gentle, wonder-filled, joyful.

    Do not include any text, letters, words, or speech bubbles in the image.

    ABSOLUTE RULE: No text, no letters, no words, no titles, no captions, 
    no watermarks, no labels anywhere in the image. 
    Completely text-free illustration only.

    """

    negative_prompt = """
    extra legs, extra arms, three legs, four legs, extra limbs, deformed limbs,
    duplicate body parts, bad anatomy, mutated, fused characters,
    reflective floor, mirror floor, glossy surface, distorted figures,
    background people, crowd, anime, cartoon, digital art, video game art,
    sharp outlines, dark lighting, scary, text, watermark, words, letters
    """
    
    # Use the inference client
    # image = client.text_to_image(
    #     prompt=prompt,
    #     negative_prompt=negative_prompt,
    #     model="black-forest-labs/FLUX.1-schnell"  # Fast free model
    # )
    
    # return image

    response = requests.post(
        f"https://api.cloudflare.com/client/v4/accounts/{st.secrets['CF_ACCOUNT_ID']}/ai/run/@cf/stabilityai/stable-diffusion-xl-base-1.0",
        headers={"Authorization": f"Bearer {st.secrets['CF_API_TOKEN']}"},
        json={"prompt": prompt}
    )
    
    image = Image.open(BytesIO(response.content))
    return image