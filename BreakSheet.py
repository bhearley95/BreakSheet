# Import Modules
import streamlit as st
import pandas as pd
import os
import glob

# Set Page Configuration
st.set_page_config(layout="wide")

# Set Title
st.title('NBA Team Breaks Sheets')
st.markdown('Select the products in your break to view the full checklist.')

# Get List of all products available
home = os.getcwd()
prod_dir = os.path.join(home,'ProductSheets')
os.chdir(prod_dir)
files_all = glob.glob('*.xlsx')
prod_all = []
for i in range(len(files_all)):
  name = files_all[i][:len(files_all)-4]
  st.markdown(name)

# Get the products
grid_prod = st.columns([0.4,0.6])
with grid_prod[0]:
  num_prod = st.number_input('Total number of products in the break',  min_value=0, max_value=None, value=0, step=1)


