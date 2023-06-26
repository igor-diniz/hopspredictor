import streamlit as st


def apply_style():
    selectbox_option_style = """
        <style>
        li {
            background-color: #dad7cd !important;
            color: #000000 !important;
        }
    
        li:hover {
            background-color: #52b788 !important;
        }
    
        .stTextInput > div > div {
            background-color: #52b788 !important;
            color: #000000 !important;
        }
    
        button {
            background-color: #dad7cd !important;
            box-shadow: none !important;
            float: right;
        }
    
        button:hover {
            color: #52b788 !important;
        }
    
        p { font-size: 16px !important; }
    
         h1 {
             padding-top: 0 !important;
         }
    
         div.css-zmkdw.esravye0 {
            padding-top: 0 !important;
         }
    
         div.block-container.css-z5fcl4.e1g8pov64 {
            padding-top: 0 !important;
         }
    
         div.css-1kyxreq.ebxwdo62 {
            display: flex;
            flex-direction: row-reverse; 
         }
    
         header.css-37pbj4.e13qjvis2 {
            display: none;
         }
    
         button.css-1l04036.e15ugz7a1 {
    
         }
    
        div.viewerBadge_link__1S137 {
            display: none;
        }
        
        </style>
    """

    # Apply custom CSS
    st.markdown(selectbox_option_style, unsafe_allow_html=True)
