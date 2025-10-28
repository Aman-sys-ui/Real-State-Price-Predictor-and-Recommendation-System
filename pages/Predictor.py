import streamlit as st
import pandas as pd
import numpy as np
import joblib
from src.utils import load_pickle

# ----------------------------------
# Load Trained Model and Reference DataFrame using shared utils
model = load_pickle("models/pipeline.pkl")
df = load_pickle("models/df.pkl")
# Provide safe defaults if df couldn't be loaded so the page still renders
if df is None:
    df = pd.DataFrame(
        {
            "sector": ["Unknown"],
            "bedRoom": [1, 2, 3],
            "bathroom": [1, 2],
            "balcony": [0, 1],
            "agePossession": ["New"],
            "furnishing_type": ["Semi-furnished"],
            "luxury_category": ["Standard"],
            "floor_category": ["Ground"],
        }
    )

# ----------------------------------
# Page Title
st.header("Gurgaon Property Price Prediction")

# ----------------------------------
# User Input Fields

# Select property type (flat or independent house)
property_type = st.selectbox("Property Type", ["flat", "independent house"])

# Choose the sector (location) from the available sectors in dataset
sector = st.selectbox("Sector", sorted(df["sector"].unique().tolist()))

# Number of bedrooms
bedroom = float(st.selectbox("Bedrooms", sorted(df["bedRoom"].unique().tolist())))

# Number of bathrooms
bathroom = float(st.selectbox("Bathrooms", sorted(df["bathroom"].unique().tolist())))

# Number of balconies
balcony = st.selectbox("Balcony", sorted(df["balcony"].unique().tolist()))

# Property age category
property_age = st.selectbox(
    "Age of Property", sorted(df["agePossession"].unique().tolist())
)

# Built-up area input
area = float(
    st.number_input("Built-Up Area (sq.ft)", min_value=200, max_value=10000, value=1000)
)

# Whether the property has a servant room
servant = float(st.radio("Servant Room", [0.0, 1]))

# Whether the property has a store room
store = float(st.radio("Store Room", [0.0, 1]))

# Furnishing type (e.g., Semi-furnished, Fully-furnished)
furnish = st.selectbox(
    "Furnishing Type", sorted(df["furnishing_type"].unique().tolist())
)

# Luxury classification (based on amenities, brand, etc.)
luxury = st.selectbox(
    "Luxury Category", sorted(df["luxury_category"].unique().tolist())
)

# Floor category (e.g., Ground, Mid, High)
floor_cat = st.selectbox(
    "Floor Category", sorted(df["floor_category"].unique().tolist())
)

# ----------------------------------
# Run Prediction
if st.button("Predict Price"):
    if model is None:
        st.error(
            "Prediction model is not available. Please provide 'pipeline.pkl' in the project root."
        )
    else:
        # Gather all inputs into a row
        data = [
            [
                property_type,
                sector,
                bedroom,
                bathroom,
                balcony,
                property_age,
                area,
                servant,
                store,
                furnish,
                luxury,
                floor_cat,
            ]
        ]

        # Ensure the same column order used during model training
        columns = [
            "property_type",
            "sector",
            "bedRoom",
            "bathroom",
            "balcony",
            "agePossession",
            "built_up_area",
            "servant room",
            "store room",
            "furnishing_type",
            "luxury_category",
            "floor_category",
        ]

        # Convert to DataFrame for model input
        one_df = pd.DataFrame(data, columns=columns)

        try:
            # Predict the price (in crores)
            prediction = model.predict(one_df)[0]
            st.success(f"Estimated Price: ₹{prediction:.2f} Cr")
        except Exception as e:
            # Catch and show errors if prediction fails
            st.error(f"Prediction Failed: {e}")
