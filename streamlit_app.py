# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col, when_matched
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie :cup_with_straw:")
st.write("""Choose the fruits you want in your smooothie!""")

#rdc = st.selectbox('Root Depth:', ('S','M','D'))

name_on_order = st.text_input('Name on Smoothie')
st.write('The name on ypur smoothie will be:', name_on_order)

cnx=st.connection("snowflake")
session = cnx.session()# Get the current credentials
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
st.dataframe(data=my_dataframe, use_container_width=True) # Shows the dataframe on the page
st.stop()

ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe, max_selections=5) # Select using dataframe, max=5
if ingredients_list:
    #st.text(ingredients_list) # Show the list in constraint format
    #st.write(ingredients_list) # Show the list in desglosed format
    
    # Convert a list to a string
    ingredients_string=''
    for fruit_chosen in ingredients_list:
        ingredients_string+=fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
        sf_df=st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    #my_insert_stmt = """ INSERT INTO smoothies.public.orders(ingredients,NAME_ON_ORDER)
            #values ('""" + ingredients_string + """','"""+name_on_order+"""')"""
    my_insert_stmt = f""" INSERT INTO smoothies.public.orders(ingredients,NAME_ON_ORDER)
            values ('{ingredients_string}','{name_on_order}')"""

    #st.write(my_insert_stmt)
    #st.stop() # To stop the execution here
    
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
