from PIL import Image
from io import BytesIO
import streamlit as st
import os
import fal_client
import requests

#os.environ["FAL_KEY"] = st.secrets["FAL_KEY"]

#client = InferenceClient(token=st.secrets['HF_TOKEN'])

def generate_image(story: str, setting :str, child_name: str = None ):

    print(story[10:])
    print(child_name)
    #name_instruction = f"featuring a child named {child_name}" 
    #name_ref = f"The main child character is named {child_name} and must be the central focus with all." if child_name else "A child protagonist must be the central focus."

    prompt = f"""
    Children's book illustration in children storybook art style, soft lighting, cute and colorful,appropriate for children.
    NOT digital cartoon. NOT glossy. NOT video game art. NOT anime.

    Scene: {story}
    Setting: {setting}

    Step 1: Identify ALL characters (people, animals, creatures) mentioned in the story.
    Step 2: Visually represent EVERY character in the scene.

    CRITICAL RULE:
    ALL characters mentioned in the story MUST appear in the illustration.
    Do NOT omit any character.
    Do NOT merge characters.
    Do NOT hide characters behind others.
    Each character must be fully visible and clearly distinct.
    The illustartion should be appropriate for children and relevant to the story.

    Character rules:
    Each human character has exactly two legs, two arms, and correct body proportions.
    Each animal or bird should have appropriate body structure.
    Characters are clearly separated and not overlapping below the waist.
    Simple clean floor with no reflections or mirror effects.

    Composition: 
    Close-up warm storybook scene, uncluttered background, 
    soft dreamy edges, protagonist fills 60% of the frame.
    Mood: Warm, gentle, wonder-filled, joyful.

    Do not include any text, letters, words, or speech bubbles in the image.

    ABSOLUTE RULE: No text, no letters, no words, no titles, no captions, 
    no watermarks, no labels anywhere in the image. 
    Completely text-free illustration only.

    """

    negative_prompt = """
    extra legs, extra arms, three legs, bad anatomy, deformed limbs,
    fused characters, fused bodies, merged characters, hybrid human animal,
    human head on animal body, animal head on human body,
    body parts mixing between characters, overlapping bodies,
    reflective floor, background crowd, extra people,
    dark lighting, scary, horror, violence, 
    text, watermark, words, letters,
    blurry, low quality, ugly, dull colors, washed out,
    anime, manga, sketch, pencil drawing
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
        json={"prompt": prompt,
              "negative_prompt": negative_prompt,
              "num_steps": 20,        # ✅ More steps = better quality
              "guidance": 8.5,        # ✅ Higher = follows prompt more strictly
              "width": 1024,          # ✅ SDXL native resolution
              "height": 1024}
    )
    
    content_type = response.headers.get("content-type", "")

    if response.status_code != 200:
        raise Exception(f"Cloudflare API error: {response.json()}")

    if "application/json" in content_type:
        data = response.json()
        if "result" in data and "image" in data["result"]:
            import base64
            image_data = base64.b64decode(data["result"]["image"])
            image = Image.open(BytesIO(image_data))
        else:
            raise Exception(f"Unexpected response: {data}")
    else:
        image = Image.open(BytesIO(response.content))

    return image
