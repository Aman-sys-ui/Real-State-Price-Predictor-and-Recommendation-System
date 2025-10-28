import pandas as pd
import pickle
import streamlit as st

# Loads model
def load_pickle(path, default=None):
    try:
        with open(path, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        st.warning(f"File not found: {path}")
        return default
    except Exception as e:
        st.error(f"Error loading {path}: {e}")
        return default


# Loads data 
def load_csv(path, default=None):
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        st.warning(f"CSV not found: {path}")
        return default
    except Exception as e:
        st.error(f"Error loading CSV {path}: {e}")
        return default

# Recommendation logic (content-based)
def get_recommendations(selected_name, df, similarity_matrix, top_n=5):
    if selected_name not in df["PropertyName"].values:
        st.error(f"Property '{selected_name}' not found in DataFrame.")
        return pd.DataFrame(), []
    idx = df[df["PropertyName"] == selected_name].index[0]
    sim_scores = list(enumerate(similarity_matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_indices = [i for i, score in sim_scores[1 : top_n + 1]]
    top_scores = [score for i, score in sim_scores[1 : top_n + 1]]
    return df.iloc[top_indices], top_scores

# Add more helpers as needed
