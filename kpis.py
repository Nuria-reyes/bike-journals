
# usage: streamlit run kpis.py

import pandas as pd
import streamlit as st
import plotly.express as px

def load_data():
    station = pd.read_csv('station.csv')
    trip = pd.read_csv('trip.csv')
    bike = pd.read_csv('bike.csv')
    people = pd.read_csv('people.csv')
    return station, trip, bike, people

def add_month_year_trip(trip):
    trip['start_date'] = pd.to_datetime(trip['start_date'])
    trip['year/month'] = trip['start_date'].dt.to_period('M').astype(str)
    trip['year/month'] = pd.to_datetime(trip['year/month'], format='%Y-%m')
    return trip

def add_duration_minute(trip):
    trip['duration_minute'] = trip['duration']/60
    return trip

def average_trip_duration(trip):
    average_trip_duration_data = trip.groupby(['year/month'])['duration_minute'].mean().round(3).reset_index()
    return average_trip_duration_data

def last_month_average_trip_duration(average_trip_duration_data):
    average_trip_duration_data_order = average_trip_duration_data.sort_values(by='year/month', ascending=False)
    last_month = average_trip_duration_data_order.iloc[0]
    previous_month = average_trip_duration_data_order.iloc[1]
    return last_month, previous_month

def calculate_average_trip_duration(trip):
    average = trip['duration_minute'].mean()
    return average

def bikes_rent(trip):
    bikes_rent_data = trip.groupby(['year/month'])['bike_number'].count().reset_index()
    bikes_rent_data.rename(columns= {'bike_number': 'bikes_rent'}, inplace = True)
    average = bikes_rent_data['bikes_rent'].mean()
    return bikes_rent_data, average

def bikes_rent_last_month(bike_rent_data):
    bike_rent_data_order = bike_rent_data.sort_values(by='year/month', ascending=False)
    last_month = bike_rent_data_order.iloc[0]
    previous_month = bike_rent_data_order.iloc[1]
    return last_month, previous_month

def aggrupate_age(trip):
    bins = [5, 18, 35, 60, float('inf')]  
    labels = ['Child', 'Young', 'Adult', 'Senior']
    trip['age_group'] = pd.cut(trip['age'], bins=bins, labels=labels, right=False)
    return trip

def aggrupate_age_bikes_rent(trip):
    age_bikes_rent = trip.groupby(['age_group'])['bike_number'].count().reset_index()
    age_bikes_rent.rename(columns={'bike_number': 'bike_rent'}, inplace=True)
    return age_bikes_rent

def bikes_rent_young(trip):
    young = trip[trip['age_group'] == 'Young']
    bikes_rent_young_data = young.groupby(['year/month'])['bike_number'].count().reset_index()
    bikes_rent_young_data.rename(columns={'bike_number': 'bike_rent'}, inplace = True)
    average = bikes_rent_young_data['bike_rent'].mean()
    return bikes_rent_young_data, average

def bikes_rent_young_last_month(bikes_rent_young_data):
    bikes_rent_young_data_order = bikes_rent_young_data.sort_values(by = 'year/month', ascending = False)
    last_month = bikes_rent_young_data_order.iloc[0]
    previous_month = bikes_rent_young_data_order.iloc[1]
    return last_month, previous_month

def bikes_rent_adult(trip):
    adult = trip[trip['age_group'] == 'Adult']
    bikes_rent_adult_data = adult.groupby(['year/month'])['bike_number'].count().reset_index()
    bikes_rent_adult_data.rename(columns={'bike_number': 'bike_rent'}, inplace = True)
    average = bikes_rent_adult_data['bike_rent'].mean()
    return bikes_rent_adult_data, average

def bikes_rent_adult_last_month(bikes_rent_adult_data):
    bikes_rent_adult_data_order = bikes_rent_adult_data.sort_values(by = 'year/month', ascending = False)
    last_month = bikes_rent_adult_data_order.iloc[0]
    previous_month = bikes_rent_adult_data_order.iloc[1]
    return last_month, previous_month

def number_trip_equal_station(trip):
    filtered_data = trip[trip['start_station'] == trip['end_station']]
    bikes_rent_data_filtered = filtered_data.groupby(['year/month'])['bike_number'].count().reset_index()
    bikes_rent_data_filtered.rename(columns= {'bike_number': 'bikes_rent'}, inplace = True)
    average = bikes_rent_data_filtered['bikes_rent'].mean()
    return bikes_rent_data_filtered, average

def bikes_rent_last_month_equal_station(bike_rent_data_filtered):
    bike_rent_data_order = bike_rent_data_filtered.sort_values(by='year/month', ascending=False)
    last_month = bike_rent_data_order.iloc[0]
    previous_month = bike_rent_data_order.iloc[1]
    return last_month, previous_month

def percentage(bikes_rent_data_filtered, bikes_rent_data):
    sum_filter = bikes_rent_data_filtered['bikes_rent'].sum()
    sum_data = bikes_rent_data['bikes_rent'].sum()
    return round((sum_filter/sum_data)*100, 3)


station, trip, bike, people = load_data()
trip = add_month_year_trip(trip)
trip = add_duration_minute(trip)
average_trip_duration_data = average_trip_duration(trip)
last_month_average_trip_duration_info, previous_month_average_trip_duration_info = last_month_average_trip_duration(average_trip_duration_data) 
average = calculate_average_trip_duration(trip)
bikes_rent_data, average_rent_data = bikes_rent(trip)
last_month_bikes_rent, previous_month_bikes_rent = bikes_rent_last_month(bikes_rent_data)
trip = aggrupate_age(trip)
age_bikes_rent = aggrupate_age_bikes_rent(trip)
bikes_rent_young_data, average_bikes_rent_young_data = bikes_rent_young(trip)
bikes_rent_young_last_month_info, bikes_rent_young_previous_month_info  = bikes_rent_young_last_month(bikes_rent_young_data)
bikes_rent_adult_data, average_bikes_rent_adult_data = bikes_rent_adult(trip)
bikes_rent_adult_last_month_info, previous_month_adult_rent_bike = bikes_rent_adult_last_month(bikes_rent_adult_data)
bikes_rent_data_equal_station, average_equal_station = number_trip_equal_station(trip)
last_month_equal_station, previous_month_equal_station = bikes_rent_last_month_equal_station(bikes_rent_data_equal_station)
percentage_filter = percentage(bikes_rent_data_equal_station, bikes_rent_data)

st.set_page_config(page_title="KPI's Dashboard", layout="wide")

col1, col2, col3, col4, col5 = st.columns(5)
with col1: 
    with st.container():
        if previous_month_average_trip_duration_info['duration_minute'] > last_month_average_trip_duration_info['duration_minute']:
            st.markdown(f"""
                        ### Average trip duration last month in minutes
                        <h1 style='color: #4CAF50;'> {last_month_average_trip_duration_info['duration_minute']} \U0001F53B</h1> 
                        """, unsafe_allow_html=True)
        else: 
            st.markdown(f"""
                        ### Average trip duration last month in minutes
                        <h1 style='color: #4CAF50;'> {last_month_average_trip_duration_info['duration_minute']} \U0001F53A</h1>
                        """, unsafe_allow_html=True)
with col2:
    with st.container():
        if previous_month_bikes_rent['bikes_rent'] > last_month_bikes_rent['bikes_rent']:
            st.markdown(f"""
                        ### Number of rented bikes last month 
                        <h1 style='color: #4CAF50;'> {last_month_bikes_rent['bikes_rent']} \U0001F53B</h1> 
                        """, unsafe_allow_html=True)

        else:
            st.markdown(f"""
                        ### Number of rented bikes last month 
                        <h1 style='color: #4CAF50;'> {last_month_bikes_rent['bikes_rent']} \U0001F53A</h1> 
                        """, unsafe_allow_html=True)
with col3:
    with st.container():
        if bikes_rent_young_previous_month_info['bike_rent']  > bikes_rent_young_last_month_info['bike_rent']:
            st.markdown(f"""
                        ### Number of rented bikes on September 2012 by young people
                        <h1 style='color: #4CAF50;'> {bikes_rent_young_last_month_info['bike_rent']} \U0001F53B</h1> 
                        """, unsafe_allow_html=True)

        else:
            st.markdown(f"""
                        ### Number of rented bikes on September 2012 by young people
                        <h1 style='color: #4CAF50;'> {bikes_rent_young_last_month_info['bike_rent']} \U0001F53A</h1> 
                        """, unsafe_allow_html=True)
            
with col4:
    with st.container():
        if previous_month_adult_rent_bike['bike_rent'] > bikes_rent_adult_last_month_info['bike_rent']:
            st.markdown(f"""
                        ### Number of rented bikes September 2012 by adult people
                        <h1 style='color: #4CAF50;'> {bikes_rent_adult_last_month_info['bike_rent']} \U0001F53B</h1> 
                        """, unsafe_allow_html=True)

        else:
            st.markdown(f"""
                        ### Number of rented bikes September 2012 by adult people
                        <h1 style='color: #4CAF50;'> {bikes_rent_adult_last_month_info['bike_rent']} \U0001F53A</h1> 
                        """, unsafe_allow_html=True)

with col5:
    with st.container():
        if previous_month_equal_station['bikes_rent'] > last_month_equal_station['bikes_rent']:
            st.markdown(f"""
                        ### Number of rented bikes that depart and arrive in the same station last month  
                        <h1 style='color: #4CAF50;'> {last_month_equal_station['bikes_rent']} \U0001F53B</h1> 
                        """, unsafe_allow_html=True)

        else:
            st.markdown(f"""
                        ### Number of rented bikes that depart and arrive in the same station last month 
                        <h1 style='color: #4CAF50;'> {last_month_equal_station['bikes_rent']} \U0001F53A</h1> 
                        """, unsafe_allow_html=True)           


col1, col2 = st.columns(2)

with col1:
    bar_chart = px.bar(average_trip_duration_data,
                   x='year/month',
                   y='duration_minute',
                   title='Average trip duration per month/year')
    
    bar_chart.add_hline(y=average, line=dict(color='red', dash='dash', width=2))
    st.plotly_chart(bar_chart)

with col2:
        bar_chart = px.bar(bikes_rent_data,
                   x='year/month',
                   y='bikes_rent',
                   title='Rented bikes per month/year')
    
        bar_chart.add_hline(y=average_rent_data, line=dict(color='red', dash='dash', width=2))
        st.plotly_chart(bar_chart)

col1, col2 = st.columns(2)

with col1:
    bar_chart = px.bar(age_bikes_rent,
                   x='age_group',
                   y='bike_rent',
                   title='Rented bikes per age group')
    st.plotly_chart(bar_chart)

with col2:
    bar_chart = px.bar(bikes_rent_young_data,
                   x='year/month',
                   y='bike_rent',
                   title='Rented bikes by young customers by year/month')
    bar_chart.add_hline(y=average_bikes_rent_young_data, line=dict(color='red', dash='dash', width=2))
    st.plotly_chart(bar_chart)

col1, col2 = st.columns(2)
with col1:
    bar_chart = px.bar(bikes_rent_adult_data,
                   x='year/month',
                   y='bike_rent',
                   title='Rented bikes by adults by year/month')
    bar_chart.add_hline(y=average_bikes_rent_adult_data, line=dict(color='red', dash='dash', width=2))
    st.plotly_chart(bar_chart)

with col2:
    bar_chart = px.bar(bikes_rent_data_equal_station,
                   x='year/month',
                   y='bikes_rent',
                   title='Rented bikes per year/month in the same station')
    bar_chart.add_hline(y=average_equal_station, line=dict(color='red', dash='dash', width=2))
    st.plotly_chart(bar_chart)

st.subheader("Conclusions:")
st.write(f"""
            
    1. At the begining we had trips with more duration but now the trips are below average.
    2. Over time, the number of rented bikes increases. We can assume that every November there will be a decrease in that number.
    3. Most of the customers belong to the young and adult groups.
    4. In the charts for the young and adult groups, we only have data up to September 2012. We can suppose that this is because the other trips are of the casual type, and the age of the person has not been recorded.
    5. {percentage_filter} of the rented bikes are used for daily tasks. """)

st.markdown(f"""
                    <style>
                    .pretty-text-final {{
                        font-family: "Lucida Console", "Courier New", monospace;
                        font-size: 15px;
                    }}
                    </style>
                    <p class="pretty-text-final"> Created by Nuria Reyes Dorta  </p>
            """, unsafe_allow_html=True)