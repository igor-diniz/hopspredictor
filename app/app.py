import streamlit as st
import pandas as pd
import pickle
import json
import charts
import images_helper

st.set_page_config(page_title="Hops Predictor", page_icon="images/logo_hopspredictor.jpeg", layout="wide")


@st.cache_data
def get_hop_varieties():
    df = pd.read_csv("data/beer_style.csv")
    select = ["Select"]
    select.extend(df["Hop variety & % rel. Oil"].unique().tolist())
    return select


@st.cache_data
def get_model():
    return pickle.load(open('models/beer_model.pkl', 'rb'))


@st.cache_data
def get_beer_style():
    return pd.read_csv('data/beer_style.csv')


def locate_beer_recipe(hop_var, prod_type):
    local_beer_style = get_beer_style()
    return local_beer_style.loc[
        (local_beer_style['Hop variety & % rel. Oil'] == hop_var) & (local_beer_style['Product Type'] == prod_type)
        ]


def predict():
    global hop_amount, hop_variety, hop_format, beer_style, model
    hop_var = hop_variety
    prod_type = hop_format
    amount = float(hop_amount)

    if prod_type == "Whole":
        prod_type = "T-90/Whole"

    if prod_type == 'T-90':
        prod_type = "T-90/Whole"

    row = locate_beer_recipe(hop_var, prod_type)

    if row.empty:
        return json.dumps({
            'No results': 'No results'
        })

    min_total_oil = row.iloc[0]['min total oil']
    min_total_oil = min_total_oil.replace(',', '.')
    min_total_oil = float(min_total_oil)
    min_total_oil = min_total_oil * amount / 100

    mini = [str(row.iloc[0]['min-geraniol']), str(row.iloc[0]['min-linalool']), str(row.iloc[0]['min-myrcene']),
            str(row.iloc[0]['min-trans-β-Farnesene']), str(row.iloc[0]['min-α-humulene']),
            str(row.iloc[0]['min-β-Caryophylene']), str(row.iloc[0]['min-β-pinene'])]
    mini = [s.replace(',', '.') for s in mini]
    mini = [float(i) for i in mini]
    mini = [min_total_oil * i * 10 for i in mini]
    print("MINI: ", mini)
    predict_min = model.predict([mini])

    max_total_oil = row.iloc[0]['max total oil']
    max_total_oil = max_total_oil.replace(',', '.')
    max_total_oil = float(max_total_oil)
    max_total_oil = max_total_oil * amount / 100

    maxi = [str(row.iloc[0]['max-geraniol']), str(row.iloc[0]['max-linalool']), str(row.iloc[0]['max-myrcene']),
            str(row.iloc[0]['max-trans-β-Farnesene']), str(row.iloc[0]['max-α-humulene']),
            str(row.iloc[0]['max-β-Caryophylene']), str(row.iloc[0]['max-β-pinene'])]
    maxi = [s.replace(',', '.') for s in maxi]
    maxi = [float(i) for i in maxi]
    maxi = [max_total_oil * i * 10 for i in maxi]
    print("MAXI: ", maxi)
    predict_max = model.predict([maxi])

    average_total_oil = row.iloc[0]['average total oil']
    average_total_oil = average_total_oil.replace(',', '.')
    average_total_oil = float(average_total_oil)
    average_total_oil = average_total_oil * amount / 100

    average = [str(row.iloc[0]['average-geraniol']), str(row.iloc[0]['average-linalool']),
               str(row.iloc[0]['average-myrcene']), str(row.iloc[0]['average-trans-β-Farnesene']),
               str(row.iloc[0]['average-α-humulene']), str(row.iloc[0]['average-β-Caryophylene']),
               str(row.iloc[0]['average-β-pinene'])]

    return json.dumps({
        'min_predictions': predict_min.tolist(),
        'max_predictions': predict_max.tolist(),
        'average_predictions': [[(min_val + max_val) / 2 for min_val, max_val in
                                zip(predict_min.tolist()[0], predict_max.tolist()[0])]]
    })


# Custom selectbox option styling
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
    
    </style>
"""

# Apply custom CSS
st.markdown(selectbox_option_style, unsafe_allow_html=True)


title_col, logo_col = st.columns([10, 1])

# Logo
with logo_col:
    images_helper.add_logo()


with title_col:
    # Title
    st.markdown("<h1 style='text-align: center;'>Hops Predictor</h1>", unsafe_allow_html=True)

    # Introduction text
    st.markdown("<h5 style='text-align: center;'>"
                "Fill out the following data fields and get a detailed forecast of your beer's aroma <br><br>"
                "</h5>", unsafe_allow_html=True)

# Text inputs
recipe_name = st.sidebar.text_input("Recipe Name")
author = st.sidebar.text_input("Author")

# Beer Information section
st.header("Beer Information")
beer_style = st.selectbox("Beer style", ["Select", "Ale", "Lager", "Stout", "IPA",
                                         "Pale Ale", "Porter", "Sour", "Wheat Beer"])

# Hops Information section
st.header("Hop Information")
hop_variety = st.selectbox("Hop variety", get_hop_varieties())
hop_format = st.selectbox("Hop format", ["Select", "Whole", "American noble", "Cryo", "T-90"])
hop_amount = st.number_input("Amount (g/L)", min_value=0.0)

st.markdown("<br><br>", unsafe_allow_html=True)

model = get_model()

# Submit button
if st.button("Predict Aromas Distribution"):
    # Check if any required field is empty
    if not beer_style or not hop_variety or not hop_format or not hop_amount:
        st.error("Please fill all both beer and hops information")
    else:
        predictions = predict()
        st.markdown("<br><br>", unsafe_allow_html=True)
        charts.draw_polygonal_chart(predictions)
        charts.draw_bar_chart(predictions)
