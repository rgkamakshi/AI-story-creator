import requests
import base64
from PIL import Image
from io import BytesIO
import streamlit as st


def generate_image(image_details):

    characters = image_details["characters"]
    scene = image_details["scene"]
    action = image_details["action"]
    objects = image_details["objects"]
    mood = image_details["mood"]

    character_description = "\n".join(
        f"- {char['name']}: {char['appearance']}"
        for char in characters
    )

    object_description = ", ".join(objects)

    prompt = f"""
    Children's book illustration in a soft, colorful storybook art style.

    CHARACTERS:
    {character_description}

    SCENE:
    {scene}

    ACTION:
    {action}

    IMPORTANT OBJECTS:
    {object_description}

    MOOD:
    {mood}

    COMPOSITION:

    All characters should be clearly visible.
    Show the characters performing the specified action.
    Make the important objects clearly visible in the scene.
    The image should visually represent the action and setting described above.
    Do not add any characters.

    Human characters should have natural child-friendly proportions.
    Animals should have appropriate anatomy.


    STYLE:

    Beautiful children's picture book illustration,
    warm and colorful,
    soft painterly textures,
    friendly expressive faces,
    whimsical,
    gentle natural lighting,
    high quality,
    clear character poses,
    full scene composition.
    """

    negative_prompt = """
    extra people, extra characters,
    extra arms, extra legs, extra fingers,
    fused characters, merged characters,
    overlapping bodies, deformed anatomy,
    hybrid human animal,
    scary, horror, violence,
    text, letters, words, watermark,
    anime, manga, video game art,
    photorealistic, dark lighting,
    blurry, low quality
    """

    # ---------------------------------
    # 3. Cloudflare FLUX.2 Klein 9B
    # ---------------------------------

    url = (
        f"https://api.cloudflare.com/client/v4/accounts/"
        f"{st.secrets['CF_ACCOUNT_ID']}/ai/run/"
        f"@cf/black-forest-labs/flux-2-klein-9b"
    )

    headers = {
        "Authorization": f"Bearer {st.secrets['CF_API_TOKEN']}"
    }

    # FLUX.2 Klein uses multipart/form-data
    data = {
        "prompt": prompt,
        "width": "1024",
        "height": "1024"
    }

    response = requests.post(
        url,
        headers=headers,
        files={
            key: (None, value)
            for key, value in data.items()
        }
    )

    # ---------------------------------
    # 4. Debug Cloudflare response
    # ---------------------------------

    print("Cloudflare status:", response.status_code)
    print("Cloudflare content type:", response.headers.get("content-type"))

    if response.status_code != 200:
        print("Cloudflare error:")
        print(response.text)

        st.error(
            f"Cloudflare image generation failed: "
            f"{response.status_code}"
        )

        return None

    # ---------------------------------
    # 5. Convert response to PIL Image
    # ---------------------------------

    try:

        result = response.json()

        print("Cloudflare response keys:", result.keys())

        image_base64 = result["result"]["image"]

        image_data = base64.b64decode(image_base64)

        image = Image.open(
            BytesIO(image_data)
        )

        return image

    except Exception as e:

        print("Could not process Cloudflare image:")
        print(e)
        print(response.text[:1000])

        st.error(
            f"Could not process generated image: {e}"
        )

        return None