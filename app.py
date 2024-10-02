import streamlit as st
from clarifai.modules.css import ClarifaiStreamlitCSS
import base64
from streamlit_card import card
import os
import streamlit.components.v1 as components





def get_image_data(img_path):
    with open(img_path, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data)
    data = "data:image/png;base64," + encoded.decode("utf-8")
    return data


def showcase():
    st.header("📚 Blogs created using AI SEO Blogger")
    blog_col_1, blog_col_2, blog_col_3 = st.columns([1, 3, 1])

    st.markdown("--- ")


    st.markdown("--- ")






st.set_page_config(page_title="AI Brand Content Creator", page_icon="📷", layout="centered")


def main():


    _, img_col, _ = st.columns([1, 3, 1])

    st.info(
        """
        **Welcome to Brander AI.ai!** 🚀

        Brander.ai is an open-source project designed to empower Brand to generate AI-driven content generation for their brand for free . It provides an extensive set of tools for creating diverse content, including blogs, images specific for your brand or company. The project aims to simplify AI-based content creation while ensuring accessibility and user-friendliness.
        """
    )

    with st.sidebar:
        _, img_col, _ = st.columns([1, 3, 1])

    st.markdown("--- ")
    st.header("🛠️ Tools")
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    st.markdown("--- ")
    # text colour blck
    blog_image_1 = get_image_data("./static/images/blog1.png")

    blog_image_2 = get_image_data("./static/images/blog2.png")

    with col1:
        hasClicked = card(
            title="📝 Store your Brand data to model",
            text="",
            image=blog_image_1,
            url="/web_crawler",
            key="blog_card",
            styles={
                "card": {
                    "width": "100%",
                },
                "title": {
                    "text-shadow": "0px 0px 1px #111111",
                    "color": "white",
                    "font-weight": "bold",
                },
                "filter": {
                    "background-color": "rgba(0, 0, 0, 0.65)"  # <- make the image not dimmed anymore
                },
            },
        )

    with col2:
        hasClicked = card(
            title="📚 TOPIC TO BLOG",
            text="",
            image=blog_image_2,
            url="/topic_to_blog",
            key="video_card",
            styles={
                "card": {
                    "width": "100%",
                },
                "filter": {
                    "background-color": "rgba(0, 0, 0, 0.65)"  # <- make the image not dimmed anymore
                },
            },
        )






if __name__ == "__main__":

    main()

