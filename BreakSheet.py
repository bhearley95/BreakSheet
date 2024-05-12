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
product_choice = []
def add_row_prod(row):
  # Select the Year
  with grid_prod[0]:
    yr_list = list(prod_dict.keys())
    yr_list.sort(reverse=True)
    while len(year_choice) < row+1:
      year_choice.append(None)
    if row == 0:
      year_choice[row] = st.selectbox('Year',yr_list, key = f'input_col_yr{row}')
    else:
      year_choice[row] = st.selectbox('Year',yr_list, key = f'input_col_yr{row}', label_visibility = "collapsed")

    # Select the Brand
    with grid_prod[1]:
      br_list = list(prod_dict[st.session_state[f'input_col_yr{row}']].keys())
      br_list.sort()
      while len(brand_choice) < row+1:
        brand_choice.append(None)
      if row == 0:
        brand_choice[row] = st.selectbox('Brand',br_list, key = f'input_col_br{row}')
      else:
        brand_choice[row] = st.selectbox('Brand',br_list, key = f'input_col_br{row}', label_visibility = "collapsed")

    # Select the Product
    with grid_prod[2]:
      pr_list = prod_dict[st.session_state[f'input_col_yr{row}']][st.session_state[f'input_col_br{row}']]
      pr_list.sort()
      while len(product_choice) < row+1:
        product_choice.append(None)
      if row == 0:
        product_choice[row] = st.selectbox('Product',pr_list, key = f'input_col_pr{row}')
      else:
        product_choice[row] = st.selectbox('Product',pr_list, key = f'input_col_br{row}', label_visibility = "collapsed")

for r in range(int(st.session_state['num_prod'])):
  add_row_prod(r)

st.markdown("""---""")

# Create Team List
team_list = ["76ers", "Bucks", "Bulls", "Cavaliers", "Celtics", "Clippers",
             "Grizzlies","Hawks","Heat","Hornets","Jazz","Kings",
             "Knicks","Lakers","Magic","Mavericks","Nets","Nuggets",
             "Pacers","Pelicans","Pistons","Raptors","Rockets","Spurs",
             "Suns","Thunder","Timberwolves","Trail Blazers","Warriors","Wizards"]
grid_team = st.columns([0.4, 0.6])
with grid_team[0]:
  team_choice = st.selectbox('Select the team',team_list,key='team_choice')

# Show the chekclist
if st.button('Show Full Break Checklist'):
  auto_data = []
  mem_data = []
  insert_data = []
  base_data = []
  for i in range(int(st.session_state['num_prod'])):
    filename = st.session_state[f'input_col_yr{i}'] + ' ' + st.session_state[f'input_col_br{i}'] + ' ' + st.session_state[f'input_col_pr{i}'] + '.xlsx'
    auto_read = pd.read_excel(os.path.join(prod_dir,filename),sheet_name = 'Autographs')
    for j in range(len(auto_read.values)):
      if st.session_state['team_choice'] in auto_read.values[j][3]:
        auto_data.append([st.session_state[f'input_col_yr{i}'], st.session_state[f'input_col_br{i}'], st.session_state[f'input_col_pr{i}'] ,
                         auto_read.values[j][0], auto_read.values[j][1], auto_read.values[j][2], auto_read.values[j][3], auto_read.values[j][4]])

    mem_read = pd.read_excel(os.path.join(prod_dir,filename),sheet_name = 'Memorabilia')
    for j in range(len(mem_read.values)):
      if st.session_state['team_choice'] in mem_read.values[j][3]:
        mem_data.append([st.session_state[f'input_col_yr{i}'], st.session_state[f'input_col_br{i}'], st.session_state[f'input_col_pr{i}'] ,
                         mem_read.values[j][0], mem_read.values[j][1], mem_read.values[j][2], mem_read.values[j][3], mem_read.values[j][4]])

    insert_read = pd.read_excel(os.path.join(prod_dir,filename),sheet_name = 'Inserts')
    for j in range(len(insert_read.values)):
      if st.session_state['team_choice'] in insert_read.values[j][3]:
        insert_data.append([st.session_state[f'input_col_yr{i}'], st.session_state[f'input_col_br{i}'], st.session_state[f'input_col_pr{i}'] ,
                         insert_read.values[j][0], insert_read.values[j][1], insert_read.values[j][2], insert_read.values[j][3], insert_read.values[j][4]])

    base_read = pd.read_excel(os.path.join(prod_dir,filename),sheet_name = 'Base')
    for j in range(len(base_read.values)):
      if st.session_state['team_choice'] in base_read.values[j][3]:
        base_data.append([st.session_state[f'input_col_yr{i}'], st.session_state[f'input_col_br{i}'], st.session_state[f'input_col_pr{i}'] ,
                         base_read.values[j][0], base_read.values[j][1], base_read.values[j][2], base_read.values[j][3], base_read.values[j][4]])

  st.markdown('Autographs')
  auto_df = pd.DataFrame(auto_data,columns = ['Year', 'Brand', 'Product', 'Card','Number', 'Player','Team','Parallels'])
  st.dataframe(auto_df, hide_index=True)

  st.markdown('Memorabilia')
  mem_df = pd.DataFrame(mem_data,columns = ['Year', 'Brand', 'Product', 'Card','Number', 'Player','Team','Parallels'])
  st.dataframe(mem_df, hide_index=True)

  st.markdown('Inserts')
  insert_df = pd.DataFrame(insert_data,columns = ['Year', 'Brand', 'Product', 'Card','Number', 'Player','Team','Parallels'])
  st.dataframe(insert_df, hide_index=True)

  st.markdown('Base')
  base_df = pd.DataFrame(base_data,columns = ['Year', 'Brand', 'Product', 'Card','Number', 'Player','Team','Parallels'])
  st.dataframe(base_df, hide_index=True)
