import pytest
import pandas as pd
import numpy as np
from src.utils import load_pickle, load_csv, get_recommendations

# Mock data for recommendation tests
def test_get_recommendations_basic():
    df = pd.DataFrame({
        "PropertyName": ["A", "B", "C", "D", "E"],
        "feature": [1, 2, 3, 4, 5],
    })
    sim_matrix = np.eye(5)
    # Make B and C most similar to A
    sim_matrix[0, 1] = 0.9
    sim_matrix[0, 2] = 0.8
    sim_matrix[0, 3] = 0.5
    sim_matrix[0, 4] = 0.2
    df_out, scores = get_recommendations("A", df, sim_matrix, top_n=2)
    assert list(df_out["PropertyName"]) == ["B", "C"]
    assert scores == [0.9, 0.8]

# Test loading functions with missing files
def test_load_pickle_missing(tmp_path):
    result = load_pickle(str(tmp_path / "missing.pkl"), default="fallback")
    assert result == "fallback"

def test_load_csv_missing(tmp_path):
    result = load_csv(str(tmp_path / "missing.csv"), default="fallback")
    assert result == "fallback"


