import streamlit as st
import pandas as pd
from src.utils import load_csv, load_pickle, get_recommendations

# ----------------------------------
# Page Configuration
st.set_page_config(page_title=" Gurgaon Apartment Recommender", layout="wide")
st.title(" Gurgaon Apartment Recommender System")
st.markdown(
    "Easily find apartments similar to your selected property using machine learning (cosine similarity)."
)

# Data loading using shared utils
df = load_csv("data/processed_apartments.csv")
similarity_matrix = load_pickle("models/similarity_matrix.pkl")


def get_recommendations(selected_name, df, similarity_matrix, top_n=5):
    # Locate the selected property by name
    idx = df[df["PropertyName"] == selected_name].index[0]

    # Retrieve similarity scores for the selected property
    sim_scores = list(enumerate(similarity_matrix[idx]))

    # Sort properties by similarity (highest first), skipping the first (self)
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_indices = [i for i, score in sim_scores[1 : top_n + 1]]
    top_scores = [score for i, score in sim_scores[1 : top_n + 1]]

    # Return top recommended properties and their similarity scores
    return df.iloc[top_indices], top_scores
## Use get_recommendations from src.utils instead


# ----------------------------------
# Property Selection Dropdown
st.subheader("Choose an Apartment")
property_names = df["PropertyName"].dropna().unique().tolist()
selected_property = st.selectbox(
    "🔍 Select a property to find similar ones:", sorted(property_names)
)

# ----------------------------------
# Show Top Recommendations
if st.button("Recommend Similar Apartments"):
    st.info("Using cosine similarity to find apartments with similar features...")

    # Get top similar apartments based on selected input
    recommended_df, scores = get_recommendations(
        selected_property, df, similarity_matrix
    )

    if recommended_df.empty:
        st.warning("No similar apartments found.")
    else:
        st.success(
            f"Top {len(recommended_df)} recommendations for **{selected_property}**:"
        )

        # Display each recommended apartment with relevant details
        for i, (index, row) in enumerate(recommended_df.iterrows()):
            st.markdown(
                f"### {i+1}. {row['PropertyName']} ({row['BHK']} BHK, {row['BuildingType']})"
            )
            st.markdown(f"**Max Area:** {row['MaxArea']} sq.ft")
            st.markdown(f"**Similarity Score:** `{round(scores[i], 3)}`")
            st.markdown(f"** Facilities:** {row['Facilities']}")
            st.markdown(f"**Nearby Landmarks:** {row['Nearby']}")
            st.write("---")
