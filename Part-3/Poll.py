# Import the libraries
import streamlit as st
import pandas as pd

# Create a title for your application using markdown syntax and Streamlit
st.title("Create a New Poll")

# Create a subheader for your application
st.subheader("You can only cast one vote")

# Bonus
library = st.radio(
    "Please select below",
    ("Yes", "No")
)

if st.button("Display selection"):
    st.write(library)
