
# usage: streamlit run api.py

import pandas as pd
import streamlit as st
import plotly.express as px

def load_data():
    station = pd.read_csv('station.csv')
    trip = pd.read_csv('trip.csv')
    people = pd.read_csv('people.csv')
    bike = pd.read_csv('bike.csv')
    return station, trip, people, bike


def calculate_average_and_total_routes(trip):
    trip = trip.drop_duplicates()
    average = trip['duration'].mean()
    total_routes = len(trip['duration'])
    return average, total_routes

def groupby_age(trip):
    trip['duration_minute'] = trip['duration']/60
    age_duration = trip.groupby(['age'])['duration_minute'].sum()
    return age_duration

def real_trip(trip):
    real_trip_data = trip[trip['duration']>60]
    return real_trip_data

def groupby_for_real_data(real_data):
    return real_data.groupby(['age'])['duration_minute'].sum()

def calculate_average_real_data(real_data):
    groupby_data = real_data.groupby(['age'])['duration_minute'].mean().reset_index()
    groupby_data.rename(columns= {'duration_minute': 'Duration'}, inplace = True)
    return round(real_data['duration_minute'].mean()), groupby_data

def registered_bike(bike):
    registered = bike[bike['sub_type']=="'Registered'"]
    return len(registered)

def groupby_bike(trip):
    number_trip_bike = trip['bike_number'].value_counts().reset_index()
    number_trip_bike.columns = ['bike_number', 'number_trips']
    return number_trip_bike

def top_10_fan_pier(station, trip):
    station_filter = station[station['station'] == 'Fan Pier']
    id = station_filter['id'].iloc[0]
    trip_filter = trip[trip['start_station'] == id]
    trip_filter = trip_filter.sort_values(by='duration', ascending=False)
    trip_filter.reset_index(drop=True, inplace=True)
    return trip_filter[['id','duration', 'start_station', 'end_station']].head(10)

def create_list_to_selector(station):
    station_names = station['station'].unique().tolist()
    return station_names

def total_trips_user_choose(trip, station, station_start):
    station_filter_1 = station[station['station'] == station_start]
    station_start_id = station_filter_1['id'].iloc[0]
    trip_filter = trip[(trip['start_station'] == station_start_id) & (trip['end_station']== station_start_id)]
    trip_from_station = len(trip[trip['start_station'] == station_start_id])
    trip_to_station = len(trip[trip['end_station'] == station_start_id])
    data = {'station_start': ['departures', 'arrivals'],
        'trips': [trip_from_station, trip_to_station]}
    df = pd.DataFrame(data)
    return len(trip_filter), df

def analysis_temporal(trip):
    trip['start_date'] = pd.to_datetime(trip['start_date'])
    trip['year/month'] = trip['start_date'].dt.to_period('M').astype(str)
    trip['year/month'] = pd.to_datetime(trip['year/month'], format='%Y-%m')
    analysis_temporal_data = trip.groupby(['year/month'])['bike_number'].count().reset_index()
    analysis_temporal_data.rename(columns={'bike_number': 'bikes_rent'}, inplace = True)
    return analysis_temporal_data

station, trip, people, bike = load_data()
average, total_routes = calculate_average_and_total_routes(trip)
age_duration = groupby_age(trip)
real_trip_data = real_trip(trip)
age_duration_real_data = groupby_for_real_data(real_trip_data)
average_real_data, groupby_data = calculate_average_real_data(real_trip_data)
registered_bike_len = registered_bike(bike)
number_trip_bike = groupby_bike(trip)
top_10_fan_pier_data = top_10_fan_pier(station, trip)
station_names = create_list_to_selector(station)
analysis_temporal_data = analysis_temporal(trip)

st.set_page_config(page_title="Bike trips Dashboard", layout="wide")


st.title('Analysis of bike trips')

st.write("""

            We have a database that has information about the different trips that a person who rents a bike does. In this database we have the following information:
            - **id**: is the id to localize the trip
            - **duration**: is the duration of the trip in seconds
            - **start_date**: is the day that starts the trip
            - **start_station**: is the station where the travel begins
            - **end_date**: is the day that finishes the trip
            - **bike_number**: is the locator of the bike
            - **sub_type**: Value which purpose is unknown. Can only take two values: 'Casual' or 'Registered'
            - **zip_code**: is the postal code of the person
            - **birth_date**: is the year when the person was born
            - **gender**: is the gender of the person
        """)

st.header('Average of duration trips and total of routes')


st.markdown(f"""The average for all routes is {round(average,3)} seconds </p>
            """, unsafe_allow_html=True)

st.markdown(f"""
            This is the total numbers of routes: {total_routes}  </p>
            """, unsafe_allow_html=True)

st.header('Minutes on bike according to the age')

st.subheader('All trips')

st.markdown('In the following table we have the sum of all the trips according to the age:')
col1, col2 = st.columns([1, 3]) 
with col1:
    st.write( age_duration)

bar_char = px.bar(age_duration.reset_index(), 
                  x = 'age',
                  y = 'duration_minute',
                  title = 'Minutes on bike according to the age',
                  )
with col2:
    st.plotly_chart(bar_char)

st.subheader('Trips with duration more than 1 minute')

st.markdown("This table has the same information that the last one but only counts the trips that take more than 1 minute")

col1, col2 = st.columns([1, 3]) 
with col1:
    st.write(age_duration_real_data)

bar_char = px.bar(age_duration_real_data.reset_index(), 
                  x = 'age',
                  y = 'duration_minute',
                  title = 'Minutes on bike according to the age but only counting the trips that take more than 1 minute',
                  color_discrete_sequence=['orange']
                  )
with col2:
    st.plotly_chart(bar_char)

st.header('Average for all real routes and number of bike registered')
st.markdown(f'The average for all the routes that we consider like real trip is {average_real_data} minutes')
st.markdown(f'The number of bikes registered is {registered_bike_len}')
st.markdown('We see the average of the trip according to the age: ')
col1, col2 = st.columns([1,3])
with col1:
    st.write(groupby_data)

with col2:
    fig = px.bar(groupby_data, x='age', y='Duration')
    st.plotly_chart(fig)
st.header('Number of trips for each bike')

st.write('In the following table, we have the number of trips that have been done for each bike: ', number_trip_bike)

st.header("Top 10 for 'Fan Pier' station")

st.write('The top 10 trips with more duration since Fan Pier station: ', top_10_fan_pier_data)

st.header("Number of trips according to the user's choice")

station_start = st.selectbox('Station: ', station_names)
#station_end = st.selectbox('End Station: ', station_names)
total_trip, data = total_trips_user_choose(trip, station, station_start)

col1, col2 = st.columns(2)

with col1:
    st.markdown(f'The total trips from {station_start} to {station_start} are {total_trip}')


fig = px.pie(data, names='station_start', values='trips', color_discrete_sequence=['#1f77b4', '#ff7f0e'])
with col2:
    st.markdown(f'In the charts, we have represented the number of trips that start in {station_start} and the number of trips that finish in {station_start}')
    st.plotly_chart(fig)

st.header('Temporal Analysis')

st.write('We want to do a temporal analysis of our data. Then, we create a new column that has the month and year when the trip started. We are interested in seeing the number of bike rents for each month.')
col1, col2 = st.columns([1, 3]) 

with col1:
    st.write(analysis_temporal_data)

bar_char = px.line(analysis_temporal_data, 
                  x = 'year/month',
                  y = 'bikes_rent',
                  title = 'Total rented bikes per month and year',
                  )
with col2:
    st.plotly_chart(bar_char)

st.subheader('Conclusion of Temporal Analysis')
st.write("""
         1. In the table, we can see that in December, January and February we didn't have records. 
         Then, we suppose that in these months the service is closed or in these months people don't rent bike.

         2. From July to October, we see a small seasonality, this can happen because it's 
         the summer holidays and people rent bikes. """)


st.markdown(f"""
                    <style>
                    .pretty-text-final {{
                        font-family: "Lucida Console", "Courier New", monospace;
                        font-size: 15px;
                    }}
                    </style>
                    <p class="pretty-text-final"> Created by Nuria Reyes Dorta  </p>
            """, unsafe_allow_html=True)
