#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
from story_generator import generate_story
from images import generate_image
import streamlit.components.v1 as components
import base64

# In[2]:

from auth import login
from mainpage import main_page

if "user" not in st.session_state:
    st.session_state["user"] = None
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None
if "story" not in st.session_state:
    st.session_state["story"] = ""
if "title" not in st.session_state:
    st.session_state["title"] = ""
if "view" not in st.session_state:
    st.session_state["view"] = "main"
if "stories" not in st.session_state:
    st.session_state["stories"] = []
if "selected_story" not in st.session_state:
    st.session_state["selected_story"] = None
if "story_ready" not in st.session_state:
    st.session_state["story_ready"] = False
if "image" not in st.session_state:
    st.session_state["image"] = None
if "story_saved" not in st.session_state:
    st.session_state["story_saved"] = False
if "guest" not in st.session_state:
    st.session_state["guest"] = False

if st.session_state["user"] is None and not st.session_state.get("guest"):
    login()
else:
    main_page()







