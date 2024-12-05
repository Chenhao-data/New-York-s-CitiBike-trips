################################################ CITIBIKES DASHABOARD ###########################################################
import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt
from numerize.numerize import numerize
from PIL import Image
import os

############################################ INITIAL SETTINGS FOR THE DASHBOARD ##################################################

st.set_page_config(page_title = 'CitiBike Strategy Dashboard', layout = 'wide')
st.title('CitiBike Strategy Dashboard')

### DEFINE SIDE BAR
st.sidebar.title('Aspect Selector')
page = st.sidebar.selectbox('Select an aspect of the analysis',
                            ['Intro page',
                             'Weather component and bike usage',
                             'Most popular stations',
                             'Interactive map with aggregated bike trips',
                             'The number of rides during each hour of the day',
                             'Recommendations'])


################################################# IMPORT DATA #####################################################################
folderpath = r"C:\Users\chenh\z_Careerfoundry\A2_DataVisal\Data\Processed data"
sample_df=pd.read_csv(os.path.join(folderpath, 'reduced_data_to_plot_7.csv'))
top_20=pd.read_csv(os.path.join(folderpath, 'top_20.csv'))
sample_aggregated=pd.read_csv(os.path.join(folderpath, 'sample_aggregated.csv'))
hourly_rides=pd.read_csv(os.path.join(folderpath, 'hourly_rides.csv'))
############################################ DEFINE THE PAGES #####################################################################

### INTRO PAGE

if page == 'Intro page':
    st.markdown(''' The project's goal is to help address the bike allocation challenges faced by Citibike Company in New York as the demand for bike-sharing services rapidly grows. Specifically, the issue is the inability to effectively allocate bikes across space and time, which has led to user complaints.''')
    st.markdown('#### Overall Approach:')
    st.markdown('1. Define Objective')
    st.markdown('2. Source Data')
    st.markdown('3. Geospatial Plot')
    st.markdown('4. Interactive Visualizations')
    st.markdown('5. Dashboard Creation')
    st.markdown('6. Findings and Recommendations')
    st.markdown('#### Dashboard Sections:')
    st.markdown('- Relationship between Daily rides and temperature')
    st.markdown('- Most popular stations')
    st.markdown('- Interactive map with aggregated bike trips')
    st.markdown('- The number of rides during each hour of the day')
    st.markdown('- Recommendations')
    st.markdown('The dropdown menu on the left under "Aspect Selector" will take you to the different aspects of the analysis our team looked at.')

    myImage = Image.open('CITIBIKE.jpg') # Source: https://unsplash.com/photos/a-row-of-bikes-parked-in-front-of-a-building-Yq2U8oTvcsQ
    st.image(myImage)
    st.markdown('Source: https://unsplash.com/photos/a-row-of-bikes-parked-in-front-of-a-building-Yq2U8oTvcsQ')

 ### Create the dual axis line chart page ###
    
elif page == 'Weather component and bike usage':

    fig_2 = make_subplots(specs = [[{"secondary_y": True}]])

    fig_2.add_trace(
    go.Scatter(x = sample_aggregated['date'], y = sample_aggregated['bike_rides_daily'], name = 'Daily bike rides', marker={'color': sample_aggregated['bike_rides_daily'],'color': 'blue'}),
    secondary_y = False
    )

    fig_2.add_trace(
    go.Scatter(x=sample_aggregated['date'], y = sample_aggregated['avgTemp'], name = 'Daily temperature', marker={'color': sample_aggregated['avgTemp'],'color': 'red'}),
    secondary_y=True
    )

    fig_2.update_layout(
    title = 'Daily bike trips and temperatures in 2022',
    height = 400
    )

    st.plotly_chart(fig_2, use_container_width=True)
    st.markdown("First, we explored the relationship between Daily rides and temperature. It is clearly evident from the chart that they show a very strong positive correlation, meaning that as the temperature rises, the number of bike uses also increases. This insight indicates that the shortage problem may be prevalent merely in the warmer months, approximately from May to October.")


### Most popular stations page

elif page == 'Most popular stations':
    
    # Bar chart
    
    fig = go.Figure(go.Bar(x = top_20['start_station_name'], y = top_20['value']))

    fig = go.Figure(go.Bar(x = top_20['start_station_name'], y = top_20['value'], marker={'color':top_20['value'],'colorscale': 'Blues'}))
    fig.update_layout(
    title = 'Top 20 Most Popular Bike Stations in NYC 2022',
    xaxis_title = 'Start stations',
    yaxis_title ='Sum of trips',
    width = 900, height = 600
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('Next, we conducted a geographic analysis and created a bar chart to display the popular stations. From the chart, the names of the stations are clearly visible. And there is a significant jump between the highest and lowest bars of the plot, indicating some clear preferences for the leading stations. ')

### MAP PAGE: INTERACTIVE MAP WITH AGGREGATED BIKE TRIPS

elif page == 'Interactive map with aggregated bike trips': 

    path_to_html = "NewYork Bike Trips Aggregated_r.html" 

    # Read file and keep in variable
    with open(path_to_html, 'r') as f: 
        html_data = f.read()

    # Show in webpage
    st.header('Aggregated Bike Trips in NYC 2022')
    st.components.v1.html(html_data,height = 1000)
    st.markdown('Next, we created an interactive map that clearly displays popular stations and routes. Based on this, we identified several popular areas.')
    st.markdown("### 1.Central Park Area")
    st.markdown('''This is New York's largest urban park with multiple cycling entrances and routes. People tend to engage in leisure and sightseeing rides here. A representative route is the circular ride from Central Park S & 6 Ave to Central Park S & 6 Ave.''')
    st.markdown("### 2.Hudson River Greenway")
    st.markdown('''Located on the west side of Manhattan, it stretches along the river and is a popular choice for sightseeing and fitness cycling. A representative route is from West St & Chambers St to Pier 40 - Hudson River Park.''')
    st.markdown("### 3.Times Square Area")
    st.markdown('''Located in the heart of Manhattan, it is densely packed with commercial and entertainment facilities. It is a primary choice for both commuter and tourist cycling. A representative route is from Broadway & W 41 St to 8 Ave & W 33 St.''')
    

### Each Hour PAGE
elif page == 'The number of rides during each hour of the day': 
   # title
    st.title("Hourly Bike Rides Analysis")

    #  # Create the filter
    selected_season = st.selectbox("Select a Season", options=hourly_rides['season'].unique())

    
    filtered_data = hourly_rides[hourly_rides['season'] == selected_season]

    # creat line chart
    fig3 = go.Figure()
    
    
    fig3.add_trace(go.Scatter(
        x=filtered_data["hour"], 
        y=filtered_data["ride_count"], 
        mode="lines+markers",  # 显示折线和标记点
        name=f"Hourly Rides ({filtered_data['season']})",
        line=dict(color='blue', width=2),  # 设置线条颜色和宽度
        marker=dict(size=8)  # 设置标记点大小
    ))
    
    
    fig3.update_layout(
        xaxis_title="Hour of Day",
        yaxis_title="Ride Count",
        template="plotly_white",  
        xaxis=dict(tickmode='linear', tick0=0, dtick=1),  
        yaxis=dict(showgrid=True)  
    )
    
    
    st.plotly_chart(fig3)
    st.markdown('Finally, we analyzed the number of rides at different times of the day, created a line chart, and added the ability to filter by season.')
    st.markdown("Generally, the number of rides begins to increase around 5 a.m., reaching the first peak at 8 a.m. After a slight decrease, it stabilizes until around 3 p.m., when it starts to rise again, peaking for the day at around 5 p.m., and then rapidly declining.")
    st.markdown("There are slight differences across seasons as well. The daily peak in winter occurs at 4 p.m., in summer at 6 p.m., while in spring and autumn, it is at 5 p.m.")


### CONCLUSIONS PAGE: RECOMMENDATIONS
else:
    
    st.header('Recommendations')
    st.markdown('Based on the above analysis, we will provide targeted recommendations for NY Citibike:')
    st.markdown('### Dynamic scheduling based on temperature and season:')
    st.markdown('####  Increase the number of bikes during the peak cycling season (from May to October) and reduce deployment in the lower-demand winter season to optimize resource utilization. And integrating weather data and real-time cycling data, predict peak demand periods (e.g., warm, sunny days) and deploy bikes in advance.')
    st.markdown('### Geographic optimization:')
    st.markdown('####  Set up dynamic dispatch stations around popular areas such as Central Park, Hudson River, and Times Square to ensure timely bike replenishment or retrieval. Additionally, supplement the bike supply in popular areas from nearby regions.')
    st.markdown('### Time-based supply and demand balance:')
    st.markdown('####  Deploy bikes in high-demand areas ahead of morning and evening peak hours (e.g., 7-9 a.m. and 4-6 p.m.). After peak hours, retrieve excess bikes to surrounding areas to avoid bike congestion at popular stations. Additionally, fine-tune peak hours based on seasonal variations.')