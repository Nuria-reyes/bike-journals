# Instructions 

To get the datasets that we use in `api.py` and `kpis.py` you have first run `preprocess_data.py` with the datasets `data_trips.txt` and `data_stations.txt` that we don't have in the repository. These datasets are what were provided to us during the interview. These datasets aren't uploaded because they are too large in size. 

First, we need these datasets in the folder.

After that, write these commands in the terminal:

- `python preprocess_data.py`

- `streamlit run api.py`

- `streamlit run kpis.py`


# Description

At the begining, we had two datasets. But, one of them isn't normalized. For this reason, we need to preprocess this data. 

The file that do this preprocess is `preprocess_data.py`. Besides preprocessing this dataset, we add the name columns of station dataset and we create two dataframe called `people.csv` and `bike.csv`. 

In the file `api.py` we have all the answers for the following questions:

- Design a dashboard in Streamlit to represent the following information: 
a.	What is the average for the duration of the trips? Total numbers of trips? 
b.	Bike trip minutes according to the client's age. 
c.	If you only take into account the real trips? This trips have a duration more than 1 minute. 
d.	The average of the real trips, but in minute, without decimals and with the heading <<Duration>>. How many bike are registered?
e.	Can you show a table with the bikes and the number of trips that have been carried out?
f.	What are the 10 longest trips that departed from the station called 'Fan Pier'?
g.	How many trips have departed from and returned to the station according to the user's selection filter?
h.	Do a temporal analysis of the data.

In the file `kpips.py` we have the answer for this question:

- Implement at least 5 business-relevant KPIs to gain a better understanding of the service provided and thus make informed decisions.

In the metrics, the triangle means if the number of the last month is better or worse that the previous month. 
In the charts, the red line is the level of crisis that I used. In this case, I'm using the average for each metrics. 

I use 5 metrics to understand the service:

1. Average trip duration in minutes: 
    - This metric helps us understand whether customers use the bicycles for long trips or short ones.    
2. Number of bikes rented:
    - This metric helps us understand how many people use this service. With this metric, we can define the different levels to know if the company has a crisis or not. 
3. Number of bikes rented by young people
    - Is the same that before but according to the group that use more the service. 
4. Number of bikes rented by adult people
    -  Is the same that before but according to the second group that use more the service. 
5. Number of rented bikes that depart and arrive in the same station: 
    - With this metric, we can know if the bike has been used for everyday tasks.

