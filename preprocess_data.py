# usage: python preprocess_data.py


import pandas as pd

def load_data():
    station = pd.read_csv('data_stations.txt', names=['id', 'station', 'municipality', 'lat', 'lng'])
    trip = pd.read_csv('data_trips.txt', 
                    names = ['id', 'duration', 'start_date', 'start_station', 'end_date', 'end_station', 'bike_number', 
                            'sub_type', 'zip_code', 'birth_date', 'gender', 'extra_col1', 'extra_col2', 'extra_col3'], 
                    dtype={'id': 'Int64', 'duration': 'Int64', 'start_station': 'Int64', 'end_station': 'Int64', 'birth_date': 'Float64', 
                           'bike_number': str, 'sub_type':str, 'zip_code':str, 'gender':str})
    trip['start_date'] = pd.to_datetime(trip['start_date'])
    trip['end_date'] = pd.to_datetime(trip['end_date'])
    trip['birth_date'] = round(trip['birth_date'])
    station['station'] = station['station'].str.strip("' ")
    return station, trip

def correct_gender_male(row):
    if row['gender'] == "'Male' ":
        row['gender'] = "'Male'"
    return row

def correct_zip_code_column(row):
    if pd.isna(row['zip_code']) and not pd.isna(row['extra_col1']):
        row['zip_code'] = row['extra_col1']
    return row

def delete_innecesary_information(trip):
    del trip['extra_col1']
    del trip['extra_col2']
    del trip['extra_col3']
    return trip

def create_Age_column(row):
    if pd.notnull(row['birth_date']) and row['birth_date'] != 0:
        row['age'] = row['start_date'].year-row['birth_date']
    return row

def build_bike_data(trip):
    bike = trip[['bike_number', 'sub_type']].drop_duplicates()
    bike['id'] = range(1, len(bike) + 1)
    return bike

def build_people_data(trip):
    people = trip[['zip_code', 'gender', 'birth_date', 'age']].drop_duplicates()
    people['id'] = range(1, len(people) + 1)
    return people

station, trip = load_data()
trip = trip.apply(correct_gender_male, axis=1)
trip = trip.apply(correct_zip_code_column, axis=1)
trip = delete_innecesary_information(trip)
bike = build_bike_data(trip)
trip['age'] = pd.NA
trip = trip.apply(create_Age_column, axis=1)
people = build_people_data(trip)
station.to_csv('station.csv', index=False, encoding='utf-8')
trip.to_csv('trip.csv', index=False, encoding='utf-8')
bike.to_csv('bike.csv', index=False, encoding='utf-8')
people.to_csv('people.csv', index=False, encoding='utf-8' )