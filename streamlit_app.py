# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col, when_matched
import requests
import pandas as pd


cnx = st.connection("snowflake")

session = cnx.session() 

# Write directly to the app
st.title(f":cup_with_straw: Customize your Smoothie! :cup_with_straw:")
st.write(
  """Choose 
  **Athe fruits you want to add in your smoothie!
  """
)

name_on_order = st.text_input('Name on Smoothie')
st.write('The name on your smoothie is : ' + name_on_order)

#option = st.selectbox('What is your favorite fruit?',('Banana', 'Strawberries', 'Peaches'))
#st.write("Your favorite fruit is  : ", option)

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
pd_df = my_dataframe.to_pandas()

st.dataframe(data=pd_df, use_container_width=True)
#st.stop()

ingredient_list = st.multiselect('choose up to 5 ing',my_dataframe, max_selections = 5)

if ingredient_list:
    #st.write(ingredient_list)
    #st.text(ingredient_list)
    ing_str = ''
    
    for fr in ingredient_list:
        ing_str += fr + ' '
        st.subheader(fr + 'Nutrition Information')

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fr, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fr,' is ', search_on, '.')
   
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+ search_on)
        #st.text(smoothiefroot_response.json())
        st_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width = True)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ing_str + """','""" + name_on_order + """')"""

    #st.write(my_insert_stmt)
    time_to_insert = st.button("complete order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, '+name_on_order+'!', icon="✅")


  
