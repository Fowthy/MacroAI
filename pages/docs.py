import streamlit as st

st.markdown("""
# MacroAI - A Personalized Nutrition Recommendation System

## Idea

MacroAI is a machine learning-based application designed to provide personalized daily nutrition recommendations. 
It calculates the optimal intake of protein and other nutrients based on a user's weight, height, age, and activity level. 
Moreover, it suggests specific foods that can help the user meet these nutritional goals.

## Problem Statement

Determining the optimal daily intake of various nutrients is a complex task that depends on many individual factors. 
Existing general guidelines do not account for personal attributes like body weight, height, age, and activity level. 
Additionally, understanding how changes in weight might affect nutritional needs over time requires a data-driven approach.

## Solution

MacroAI addresses this problem by using a machine learning model trained on a dataset of nutritional recommendations. 
The model predicts the daily intake of protein and other nutrients based on the user's weight, height, age, and activity level. 
It also suggests specific foods that are rich in these nutrients. 
The system visualizes how a user's nutritional needs might change as their weight changes over time, providing a dynamic and personalized nutrition plan.

## Impact

MacroAI empowers users to make informed decisions about their diet and health. 
By providing personalized nutrition recommendations and suggesting specific foods to meet these goals, 
MacroAI can lead to improved health outcomes and a better understanding of the relationship between diet and health.

## Future Steps

The current version of MacroAI is based on a dataset of 1000 nutritional recommendations scraped from a website. 
Future work will focus on expanding this dataset to include more variety and more data points. This will improve the accuracy and applicability of the model's predictions. 
Additionally, we plan to collaborate with medical experts to validate the model's recommendations. 
Rigorous testing and validation will be conducted to ensure the accuracy of the data and the effectiveness of the recommended foods.
""")