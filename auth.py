import streamlit as st
from supabase_client import supabase
from dotenv import load_dotenv
load_dotenv()
from mainpage import main_page

st.set_page_config(page_title = "AI powered children's story creator",page_icon="✨")


def login():

    st.title("✨ AI Children's Story Creator 📚")
    st.write("Create magical, personalized stories for kids using AI.")

    tab1, tab2, tab3 = st.tabs(["Login", "Sign Up", "Try as guest"])
    with tab1:
        with st.form("login_form"):
            email = st.text_input("Enter your email")
            password = st.text_input("Enter  your Password", type="password")
            login_button = st.form_submit_button("Login")   
        # signup_button = st.form_submit_button("Signup")

            
            if login_button:
                if not email or not password:
                    st.error("Please enter all fields")
                else:
                    try:
                        response = supabase.auth.sign_in_with_password({
                        "email": email,
                        "password": password
                        })
                        if response.user:
                            st.session_state.user = response.user
                            st.session_state["user_id"] = response.user.id
                            st.success("Logged in!")
                            st.rerun()
                            
                    except Exception as e:
                        st.error("Invalid credentials")

    with tab2:
        with st.form("signup form"):  
            new_email = st.text_input("Enter your email")
            new_password = st.text_input("Enter  your Password", type="password")
            confirm_password = st.text_input("Confirm  your Password", type="password")
            signup_button = st.form_submit_button("Sign up")  

            if signup_button:
                if not new_email or not new_password or not confirm_password:
                    st.error("Please enter all the fields")
                elif new_password != confirm_password:
                    st.error("Please enter all the fields")
                elif len(new_password) < 6:
                    st.error("The Password should be atleast 6 characters")
                else:
                    try:
                        response = supabase.auth.sign_up({
                            "email": new_email,
                            "password": new_password
                        })
                        if response.user:
                            supabase.table("users").insert({
                                "id": response.user.id,
                                "email": new_email,
                                "created_at": str(response.user.created_at)
                            }).execute()
                            st.success("Account created! Please check your email to verify your account, then login.")
                    except Exception as e:
                        st.error(f"Signup failed: {e}")

    with tab3:
        st.markdown("### 👀 Try as Guest")
        st.write("Explore the story creator without signing up!")
        st.warning("⚠️ Guest stories won't be saved. Sign up to keep your stories!")
    
        if st.button("Try as Guest", use_container_width=True):
            st.session_state["guest"] = True
            st.rerun()