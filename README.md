# Gurgaon Real Estate Price Predictor & Recommendation System

A Streamlit-powered dashboard for exploring, predicting, and recommending properties in Gurgaon using machine learning and interactive visualizations.

---

## 🌟 Features

- Interactive analytics dashboard for Gurgaon real estate  
- Price prediction using a trained ML model  
- Apartment recommender system (content-based)  
- Wordcloud of common property features  
- Visualizations: sector-wise price map, area vs price, BHK distribution, and more  

---

## 🧩 Project Structure

```
gurgaon-real-estate-price-predictor/
├── app.py
├── requirements.txt
├── Dockerfile
├── README.md
├── data/
│   ├── data_viz1.csv
│   ├── processed_apartments.csv
│   └── feature_text.pkl
├── models/
│   ├── pipeline.pkl
│   ├── df.pkl
│   └── similarity_matrix.pkl
├── pages/
│   ├── home.py
│   ├── predictor.py
│   └── recommend.py
├── src/
│   └── utils.py
├── tests/
│   └── test_utils.py
```

---

## ⚙️ Setup Instructions

1. Clone the repository  
   `git clone https://github.com/yourusername/gurgaon-real-estate-price-predictor.git`  
   `cd gurgaon-real-estate-price-predictor`

2. Install dependencies  
   `pip install -r requirements.txt`

3. Prepare data and models  
   Place the required CSV and PKL files into the `data` and `models` folders respectively.

4. Run the Streamlit app  
   `streamlit run app.py`

---

## 🐳 Docker Setup

To run the app using Docker:

`docker build -t real-estate-app .`  
`docker run -p 8501:8501 real-estate-app`

---

## ⚙️ Configuration

- All data files go in `data/`  
- All model files go in `models/`  
- Environment variables can be placed in a `.env` file (supports `python-dotenv`)  

---

## 🤝 Contributing

1. Fork the repository  
2. Create a new branch for your update  
3. Commit your changes  
4. Push your branch  
5. Open a pull request  

---

## 📄 License

This project is licensed under the MIT License.

---

## 📬 Contact

For any questions or suggestions, reach out at:  
**amanak52141@gmail.com**

---