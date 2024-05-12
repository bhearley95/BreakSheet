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
home = '/mount/src/breaksheet'
prod_dir = '/mount/src/breaksheet/ProductSheets'
os.chdir(prod_dir)
files_all = glob.glob('*.xlsx')
prod_dict = {}
for i in range(len(files_all)):
  name = files_all[i][:len(files_all[i])-5]
  data = name.split(' ')
  year = data[0]
  brand = data[1]
  product = name[len(year) + len(brand) + 2:]
  # Set Up Dictionary
  year_keys = list(prod_dict.keys())
  if year not in year_keys:
    prod_dict[year] = {}
  brand_keys = list(prod_dict[year].keys())
  if brand not in brand_keys:
    prod_dict[year][brand] = []
  prod_keys = prod_dict[year][brand]
  if product not in prod_keys:
    prod_dict[year][brand].append(product)
os.chdir(home)

# Get the products
grid_num_prod = st.columns([0.4,0.6])
with grid_num_prod[0]:
  num_prod = st.number_input('Total number of products in the break',  min_value=0, max_value=None, value=0, step=1, key='num_prod')

grid_prod = st.columns([0.2,0.2,0.4,0.2])
year_choice = []
brand_choice = []
def add_row_prod(row):
  with grid_prod[0]:
    while len(year_choice) < row+1:
      year_choice.append(None)
    if row == 0:
      year_choice[row] = st.selectbox('Year',(list(prod_dict.keys()).sort().flip()), key = f'input_col_yr{row}')
    else:
      year_choice[row] = st.selectbox('Year',(list(prod_dict.keys()).sort().flip()), key = f'input_col_yr{row}', label_visibility = "collpased")
  with grid_prod[1]:
    while len(brand_choice) < row+1:
      brand_choice.append(None)
    if row == 0:
      brand_choice[row] = st.selectbox('Brand',(list(prod_dict[st.session_state[f'input_col_yr{row}']].keys()).sort()), key = f'input_col_br{row}')
    else:
      brand_choice[row] = st.selectbox('Brand',(list(prod_dict[st.session_state[f'input_col_yr{row}']].keys()).sort()), key = f'input_col_br{row}', label_visibility = "collpased")

for r in range(int(st.session_state['num_prod'])):
  add_row_prod(r)
