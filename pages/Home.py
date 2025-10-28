import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
from src.utils import load_csv, load_pickle

# Page configuration
st.set_page_config(page_title="Gurgaon Real Estate Insights", layout="wide")

# Title and introduction
st.title("Gurgaon Real Estate Analytics Dashboard")
st.markdown(
    """
    Welcome to your one-stop dashboard to explore **Gurgaon’s real estate landscape**!
    Dive into property prices, discover common features, compare property types, and get actionable insights — all in a visual and interactive way.
    """
)

DATA_PATH = "data/"
new_df = load_csv(f"{DATA_PATH}data_viz1.csv")
feature_text = load_pickle(f"{DATA_PATH}feature_text.pkl")

# Average stats by sector
group_df = new_df.groupby("sector").mean(numeric_only=True)[
    ["price", "price_per_sqft", "built_up_area", "latitude", "longitude"]
]

# Sector-wise Price Per Sqft Map
st.header("Sector-wise Price per Sqft on Map")
st.markdown(
    "Explore how property prices vary across different sectors in Gurgaon. Hover over the bubbles to see the details!"
)
fig = px.scatter_mapbox(
    group_df,
    lat="latitude",
    lon="longitude",
    color="price_per_sqft",
    size="built_up_area",
    color_continuous_scale=px.colors.cyclical.IceFire,
    zoom=10,
    mapbox_style="open-street-map",
    width=1200,
    height=700,
    hover_name=group_df.index,
)
st.plotly_chart(fig, use_container_width=True)

# Wordcloud of Common Features
st.header("☁️ Most Common Property Features")
st.markdown(
    "Here's a wordcloud of the most commonly mentioned features in Gurgaon listings — the bigger the word, the more frequent it is!"
)
wordcloud = WordCloud(
    width=800,
    height=800,
    background_color="black",
    stopwords={"s"},
    min_font_size=10,
).generate(feature_text)
fig_wc, ax_wc = plt.subplots(figsize=(8, 8))
ax_wc.imshow(wordcloud, interpolation="bilinear")
ax_wc.axis("off")
st.pyplot(fig_wc)

# Area vs Price Scatter Plot
st.header("Area vs Price (Interactive View by Property Type)")
st.markdown(
    "Select a property type to see how area and price relate across listings. You can also see how bedroom count plays a role."
)
property_type = st.selectbox("Choose Property Type:", ["flat", "house"])
filtered_df = new_df[new_df["property_type"] == property_type]
fig1 = px.scatter(
    filtered_df,
    x="built_up_area",
    y="price",
    color="bedRoom",
    title=f"Area vs Price for {property_type.capitalize()}s",
)
st.plotly_chart(fig1, use_container_width=True)

# Bedroom Distribution by Sector
st.header("Bedroom (BHK) Distribution Pie Chart")
st.markdown(
    "Curious about how many 1BHKs or 3BHKs are available? Select a sector or view overall distribution."
)
sector_options = new_df["sector"].unique().tolist()
sector_options.insert(0, "Overall")
selected_sector = st.selectbox("Select Sector:", sector_options)
pie_df = (
    new_df
    if selected_sector == "Overall"
    else new_df[new_df["sector"] == selected_sector]
)
fig2 = px.pie(pie_df, names="bedRoom", title=f"BHK Distribution - {selected_sector}")
st.plotly_chart(fig2, use_container_width=True)

# Price Comparison Across BHKs
st.header("BHK-wise Price Distribution (Box Plot)")
st.markdown(
    "See how property prices vary with the number of bedrooms. Useful for budgeting and investment planning!"
)
fig3 = px.box(
    new_df[new_df["bedRoom"] <= 4],
    x="bedRoom",
    y="price",
    title="Price Range by BHK (up to 4 BHK)",
)
st.plotly_chart(fig3, use_container_width=True)

# House vs Flat: Price Distribution
st.header("Price Comparison: House vs Flat")
st.markdown(
    "Wondering which type of property costs more? Let’s compare house and flat price distributions side-by-side."
)
fig4, ax4 = plt.subplots(figsize=(10, 4))
sns.histplot(
    new_df[new_df["property_type"] == "house"]["price"],
    label="House",
    kde=True,
    color="blue",
)
sns.histplot(
    new_df[new_df["property_type"] == "flat"]["price"],
    label="Flat",
    kde=True,
    color="green",
)
plt.title("Price Distribution: House vs Flat")
plt.xlabel("Price")
plt.ylabel("Count")
plt.legend()
st.pyplot(fig4)

# Footer
st.markdown("---")
st.markdown("Built with Streamlit | Data Source: Gurgaon Property Listings")
