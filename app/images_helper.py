import streamlit as st

def add_logo():

    st.markdown(
        """
        <div>
            <img src="images/logo_hopspredictor.jpeg"/>
        </div>
        """,
        unsafe_allow_html=True
    )
