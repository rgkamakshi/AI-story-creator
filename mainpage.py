import streamlit as st
from story_generator import generate_story
from images import generate_image
import streamlit.components.v1 as components
from supabase_client import supabase
from datetime import datetime, timezone
from PIL import Image
from io import BytesIO
import base64
from dotenv import load_dotenv
load_dotenv()

def main_page():
    st.sidebar.title("Menu")

    if st.sidebar.button("Home"):
        st.session_state["view"] = "main"
        st.rerun()

    # if st.sidebar.button("My Profile"):
    #     st.write("This is the Dashboard")

    if st.sidebar.button("My Stories"):
        try:
            user_id = st.session_state["user"].id
            response = supabase.table("stories")\
                .select("*")\
                .eq("user_id", user_id)\
                .order("created_at", desc=True)\
                .execute()

            stories = response.data or []

            if len(stories) > 0:
                st.session_state["view"] = "stories_list"
                st.session_state["stories"] = stories
                st.rerun()
            else:
                st.info("No saved stories yet!")
        except Exception as e:
            st.error(f"Failed to load stories: {e}")

    # ── STORIES LIST PAGE ──────────────────────────────────────────────
    if st.session_state.get("view") == "stories_list":
        st.markdown("## 📚 My Stories")
        st.divider()
        for i, s in enumerate(st.session_state.get("stories", [])):
            created = s.get("created_at")
            date = created[:10] if created else "Unknown date"
            title = s.get("title") or f"Story from {date}"
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.markdown(f"### 📖 {title}")
                st.caption(f"Saved on {date}")
            with col2:
                if st.button("Read →", key=f"read_{i}"):
                    st.session_state["view"] = "single_story"
                    st.session_state["selected_story"] = s
                    st.rerun()
            with col3:
                if st.button("🗑️", key=f"delete_{i}"):  # ✅ Delete button
                    st.session_state[f"confirm_delete_{i}"] = True
                    st.rerun()

            if st.session_state.get(f"confirm_delete_{i}"):
                st.warning(f"Delete **{title}**?")
                yes_col, no_col = st.columns([1, 1])
                with yes_col:
                    if st.button("Yes", key=f"yes_{i}"):
                        try:
                            supabase.table("stories")\
                                .delete()\
                                .eq("id", s["id"])\
                                .execute()
                            st.session_state["stories"].pop(i)
                            st.session_state.pop(f"confirm_delete_{i}", None)
                            st.rerun()
                        except Exception as e:
                            st.error(f"Failed to delete: {e}")
                with no_col:
                    if st.button("No", key=f"no_{i}"):
                        st.session_state.pop(f"confirm_delete_{i}", None)
                        st.rerun()

            st.divider()
        if st.button("← Back to Home"):
            st.session_state["view"] = "main"
            st.rerun()
        return

    # ── SINGLE STORY PAGE ─────────────────────────────────────────────
    if st.session_state.get("view") == "single_story":
        s = st.session_state.get("selected_story", {})
        created = s.get("created_at")
        date = created[:10] if created else "Unknown date"
        title = s.get("title") or f"Story from {date}"

        st.markdown(f"# 📖 {title}")
        st.caption(f"Saved on {date}")
        st.write(s.get("story_text", ""))
        st.divider()

            # ✅ Display image
        if s.get("image"):
            try:
                image_data = base64.b64decode(s["image"]+ "==")
                image = Image.open(BytesIO(image_data))
                st.image(image, use_container_width=True)
            except Exception as e:
                st.warning(f"Could not load image: {e}")

        
        st.divider()

        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("← Back to My Stories"):
                st.session_state["view"] = "stories_list"
                st.rerun()
        with col2:
            components.html("""
                <script>
                    function print_page(obj) {
                        obj.style.display = "none";
                        parent.window.print();
                    }
                </script>
                <button onclick="print_page(this)" style="
                    background-color: #ff4b4b;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 6px;
                    cursor: pointer;
                    font-size: 14px;">
                    🖨️ Print / Save as PDF
                </button>
            """, height=50)
        return

    # ── MAIN PAGE ─────────────────────────────────────────────────────
    st.header("Story Details")
    child_name = st.text_input("Child's name")
    age = st.number_input("Child's age (Age must be between 2 - 12)", value=2)
    if age < 2 or age > 12:
        st.error("Age should be between 2 and 12")
    characters = st.text_input("Enter the name of Character (e.g, bluey, peppa, anna)")
    setting = st.text_input("Setting (e.g, in a magical forest, in outer space, at the park)")
    tone = st.selectbox("Tone of the story", ['calming', 'funny', 'adventurous', 'silly', 'compassionate', 'exciting'])
    length = st.selectbox("Length", ['Short', 'Medium', 'Long', 'Chapter format'])
    generate_button = st.button("Create Story ✨")
    #eebutton = st.button("Save Button"/

    if generate_button:
        if not child_name and not characters:
            st.warning("Please fill in required fields")
        else:
            with st.spinner("Creating your magical story..."):
                story_gen = generate_story(child_name, age, characters, setting, tone, length)
                image_gen = generate_image(story_gen, setting, child_name)
                st.session_state["story"] = story_gen
                st.session_state["title"] = f"{child_name}'s {tone} story"
                st.session_state["image"] = image_gen
                st.session_state["story_ready"] = True
                st.session_state["story_saved"] = False


            # components.html("""
            #     <script>
            #         function print_page(obj) {
            #             obj.style.display = "none";
            #             parent.window.print();
            #         }
            #     </script>
            #     <button onclick="print_page(this)">
            #         Print page (choose 'Save as PDF' in print dialogue)
            #     </button>
            # """)

    if st.session_state.get("story_ready"):
        st.header("Your Story")
        st.write(st.session_state["story"])
        st.image(st.session_state["image"])
        
            
        col1, col2 = st.columns([4, 1])
        with col2:
            if st.session_state.get("guest"):
            # ✅ Show sign up nudge instead of save button
                st.info("🔒 Sign up to save your stories!")
                if st.button("Sign Up"):
                    st.session_state["guest"] = False
                    st.session_state["view"] = "login"
                    st.rerun()
            elif st.session_state.get("story_saved"):
                   st.success("Story saved!")
            else:
                if st.button("Save Story"):
                    try:
                        buffer = BytesIO()
                        st.session_state["image"].save(buffer, format="PNG")
                        image_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
                        supabase.table("stories").insert({
                            "user_id": st.session_state["user"].id,
                            "created_at": datetime.now(timezone.utc).isoformat(),
                            "story_text": st.session_state["story"],
                            "title": st.session_state.get("title", ""),
                            "image":image_b64
                        }).execute()
                        # st.success("Story saved!")
                        # st.session_state["story_ready"] = True
                        # st.rerun()
                        st.session_state["story_saved"] = True  # ✅ This was missing
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to save: {e}")