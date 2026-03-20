import os
from groq import Groq
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")


client = Groq(api_key=groq_api_key)


def generate_story(child_name,age,characters,setting,tone,length):
    if st.session_state.get("guest"):
        count = st.session_state.get("guest_image_count", 0)
        if count >= 1:
            st.warning("Please sign up for unlimited stories!")
            st.info("🔒 Sign up to save your stories!")
            if st.button("Sign Up"):
                st.session_state["guest"] = False
                st.session_state["view"] = "login"
                st.rerun()
            st.stop()
        else:
            st.session_state["guest_image_count"] = count + 1
    # print("inside function")
    # print(f"characters name is {characters}")
    # print(f"setting is in the {setting}")
    prompt = f"""
            Write a childrens story for child named {child_name} who is {age} years old.
            Include these characters : {characters}.
            Set the story in : {setting}.
            Write the story with a strong, consistent {tone} tone. Every element—dialogue, descriptions, pacing, and emotional beats—should reinforce that tone from beginning to end.
            The story should be {length} in length.

            Requirments:

            The sentence should be short and easy to read for a child for their age level.
            Use appropriate words and language suitable for child.
            Make the plot imaginative and engaging.
            Structure the story in clear paragraph.
           
            
         
            """

    if "illustration" in prompt.lower():
        generate_image(child_name, story_gen)

    response = client.chat.completions.create(

                model = 'llama-3.1-8b-instant',
                messages = [{"role":"user", "content":prompt}]
                
            )
    print("function reached")
# Include an animal in the story based on : {animal}.
#story = response.choices[0].message["context"]
    story = response.choices[0].message.content
    return story
