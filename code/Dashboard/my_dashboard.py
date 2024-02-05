import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from IPython.display import clear_output
import seaborn as sns
from ipywidgets import interact, widgets
from IPython.display import display, clear_output
from PIL import Image
import base64


import base64



# Title
st.title('Elephant Death Patterns')

# Data loading
df=pd.read_csv(r'..\..\data\Cleaned_data\cancat.csv')
# Load Sri Lankan district boundaries
districts = gpd.read_file(r'..\..\data\Map_file\District_geo.json')  # Specify the path to your GeoJSON file

# Group by 'District' and count the number of elephant deaths in each district
elephant_deaths_by_district1 = df['District'].value_counts().reset_index()
elephant_deaths_by_district1.columns = ['District', 'ElephantDeaths']
#df2=pd.DataFrame(elephant_deaths_by_district)
# Rename the 'ADM2_EN' column to 'District' in the GeoJSON data
districts.rename(columns={'ADM2_EN': 'District'}, inplace=True)
# Remove the 'unknown' district
districts = districts[districts['District'] != '[unknown]']
# Merge the data with district boundaries data
merged_data = districts.merge(elephant_deaths_by_district1, on='District', how='left')

# Fill NaN values with 0 for districts with no recorded elephant deaths
merged_data['ElephantDeaths'].fillna(0, inplace=True)
#st.snow()
# Sidebar (if needed)
st.sidebar.header('Settings')
option = st.sidebar.selectbox('Select an option', ('Option 1', 'Option 2', 'Option 3'))

# Main content
if option == 'Option 1':
    st.subheader('Data Table')
    st.write(df)  # Display a data table

elif option == 'Option 2':
    st.subheader('Data Visualization - Maps and Year Selector')

    # Create two columns for maps
    col1, col2 = st.columns(2)
    

    # Map 1 - Left side
    with col1:
        fig1, ax1 = plt.subplots(1, 1, figsize=(12, 10))
        merged_data.plot(column='ElephantDeaths', cmap='Reds', linewidth=0.8, edgecolor='0.8', legend=True, ax=ax1)
        merged_data.apply(lambda x: ax1.annotate(text=x['District'], xy=x.geometry.centroid.coords[0], ha='center', va='bottom'), axis=1)
        merged_data.apply(lambda x: ax1.annotate(text=str(int(x['ElephantDeaths'])), xy=x.geometry.centroid.coords[0], ha='center', va='top'), axis=1)
        ax1.set_title('Map 1: Elephant Deaths by District in Sri Lanka 2010-2018')
        st.pyplot(fig1)

    with col2:   
        if st.checkbox("Show Histogram"):
            sns.set(style="whitegrid")
            plt.figure(figsize=(12, 10))
            sns.barplot(data=elephant_deaths_by_district1, x='District', y='ElephantDeaths')
            plt.xticks(rotation=90)  # Rotate x-axis labels for better visibility
            plt.title('Elephant Deaths over District',fontsize=21)
                # Display the plot in Streamlit
            st.pyplot(plt)


elif option == 'Option 3':
    st.subheader('Data Visualization - Maps and Year Selector')

    # Create two columns for maps
    col1, col2 = st.columns(2)

    # Select box for choosing the year
    selected_year = st.selectbox('Select a Year', [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017])

    # Map 1 - Left side
    with col1:
        def update_map(year):
            # Clear the previous output
            clear_output(wait=True)

            # Load your elephant deaths data for the selected year
            data_path = f'..\..\data\Cleaned_data\{year}_clean.csv'  # Specify the path to your data
            df = pd.read_csv(data_path)

            # Group by 'District' and count the number of elephant deaths in each district
            elephant_deaths_by_district = df['District'].value_counts().reset_index()
            elephant_deaths_by_district.columns = ['District', 'ElephantDeaths']

            # Merge the data with district boundaries data
            merged_data = districts.merge(elephant_deaths_by_district, on='District', how='left')

            # Fill NaN values with 0 for districts with no recorded elephant deaths
            merged_data['ElephantDeaths'].fillna(0, inplace=True)

            # Set up the plot
            fig2, ax2 = plt.subplots(1, 1, figsize=(12, 10))
            merged_data.plot(column='ElephantDeaths', cmap='Greens', linewidth=0.8, edgecolor='0.8', legend=False, ax=ax2)
            merged_data.apply(lambda x: ax2.annotate(text=x['District'], xy=x.geometry.centroid.coords[0], ha='center', va='bottom'), axis=1)
            merged_data.apply(lambda x: ax2.annotate(text=str(int(x['ElephantDeaths'])), xy=x.geometry.centroid.coords[0], ha='center', va='top'), axis=1)
            ax2.set_title(f'Map 2: Elephant Deaths by District in Sri Lanka {year}')
            st.pyplot(fig2)
            with col2:   
                if st.checkbox("Show Histogram"):
                    sns.set(style="whitegrid")
                    plt.figure(figsize=(12, 10))
                    sns.barplot(data=elephant_deaths_by_district, x='District', y='ElephantDeaths')
                    plt.xticks(rotation=90)  # Rotate x-axis labels for better visibility
                    plt.title(f'Elephant Deaths over District in {year}',fontsize=21)
                        # Display the plot in Streamlit
                    st.pyplot(plt)
        #year_slider = st.slider(label='Year',value=2010, min_value=2010, max_value=2017, step=1)

        #interact(update_map, year=year_slider)
        update_map(selected_year)
    

