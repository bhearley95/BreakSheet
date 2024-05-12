# Import Modules
import streamlit as st
import pandas as pd

# Set Page Configuration
st.set_page_config(layout="wide")

# Set Title
st.title('NBA Team Breaks Sheets')
st.markdown('Select the products in your break to view the full checklist.')

# Get the products
num_prod = st.number_input('Total number of products in the break',  min_value=0, max_value=None, value=0, step=1)
