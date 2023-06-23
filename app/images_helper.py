from PIL import Image, ImageDraw, ImageOps
import streamlit as st

def add_logo():
    # Open the logo image
    logo_image = Image.open('images/logo-2.jpeg')

    # Define the desired output size for the circular logo
    logo_size = (85, 85)  # Adjust the size as per your preference

    # Resize the logo with a high-quality resampling method
    logo_image = logo_image.resize(logo_size, resample=Image.LANCZOS)

    # Create a circular mask
    mask = Image.new('L', logo_size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + logo_size, fill=255, outline=0)

    # Apply the circular mask to the logo image
    circular_logo = ImageOps.fit(logo_image, mask.size, centering=(0.5, 0.5))
    circular_logo.putalpha(mask)

    # Add the circular logo image to the top right corner
    st.image(circular_logo, use_column_width=False, clamp=True, width=logo_size[0])
