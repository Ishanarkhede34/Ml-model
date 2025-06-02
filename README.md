# 🍽️ Zomato Restaurant Rating Predictor

A machine learning project that predicts the **rating category** (like *Excellent*, *Good*, *Average*, etc.) of a restaurant based on various features such as cuisine, service availability, price range, and customer votes — all using real Zomato data.

This project includes a user-friendly **desktop GUI built with Tkinter** that allows interactive rating prediction by selecting a restaurant and adjusting input features.

---

## 📂 Project Overview

- **Dataset**: `zomato.csv` – contains restaurant details scraped from Zomato via Kaggle.
- **Model Logic**: `model.py` – handles data cleaning, feature encoding, scaling, and model training.
- **Application GUI**: `gui.py` – an interactive interface for predicting restaurant rating categories.

---

## 🎯 Objective

To train a machine learning model that learns from historical restaurant data and predicts the **rating category** (e.g., *Excellent*, *Good*, *Poor*) using features such as:
- Location (City)
- Cuisine type
- Table booking availability
- Online delivery support
- Pricing and votes

---

## ⚙️ Features

✅ Cleans and preprocesses real-world restaurant data  
✅ Encodes both categorical and binary features  
✅ Trains a Logistic Regression model with scaled features  
✅ Displays dynamic dropdowns for city and restaurant selection  
✅ Automatically loads restaurant details for prediction  
✅ Lets users modify inputs to experiment with different scenarios  
✅ Predicts the restaurant's rating category with a single click

---

