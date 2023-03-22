# Performing Data transformation and analysis on weather api with current weather data to analyze cities current weather status in Canada
import requests
import json
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import pandas as pd
from plotly.graph_objs import Scattergeo, Layout
from plotly import offline
import matplotlib.cm as cm
import matplotlib.colors as colors
import datetime
import plotly.graph_objs as go

my_api = "c50eecdc74b995de2330ad284965a446"  # api key

cities = [
  'Toronto', 'Montreal', 'Vancouver', 'Calgary', 'Edmonton', 'Ottawa',
  'Winnipeg', 'Quebec City', 'Hamilton', 'Kitchener', 'London', 'Victoria',
  'Halifax', 'Oshawa', 'Windsor', 'Saskatoon', 'St. Catharines', 'Regina',
  'St. Johns', 'Kelowna'
]  # list of cities
country_code = "CA"  # country code
url = "api.openweathermap.org/data/2.5/weather?q={city name},{country code}&appid={API key} "  # api url
weather_data = []  # an empty list to store weather data for each city
# looping through each city in Canada.
for city in cities:
  # Constructed the API URL
  url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&appid={my_api}"

  # Make the API call
  response = requests.get(url)

  # Checks if the API call was successful
  try:
    response.status_code == 200
    # Store the weather data for the city in the list
    weather_data.append(response.json())
    # print(weather_data)
  except:
    # Print an error message if the API call failed
    print(f"Unable to retrieve the weather data for {city}")
# writing weather data into a json file
filename = "data.json"
with open(filename, "w") as file:
  json.dump(weather_data, file)
# reading data.json file to answer given questions
with open(filename, "r") as file:
  weather_data = json.load(file)

# Question 1
print('Question 1\n')
# A. Using Scattergeo, plot the current temperature in the aforementioned cities. The plot should have:
# a. Title (do not use the same title I have in the sample image)
# b. Adjust the marker size according to the temperature
# c. Adjust the marker colour according to the temperature (any colour scale you like) d. Add a colour bar to the figure
# e. Don’t forget to specify the unit of measure for the metric
lats = []
lons = []
current_ts = []
for city_w in weather_data:  # loops through weather data
  lat = city_w['coord']['lat']
  lon = city_w['coord']['lon']
  current_t = city_w['main']['temp']
  lons.append(lon)
  lats.append(lat)
  current_ts.append(current_t)
data = [{
  'type': 'scattergeo',
  'lon': lons,
  'lat': lats,
  'marker': {
    'size': [0.2 * mag for mag in current_ts],
  },
}]
my_layout = Layout(title='20 cities in Canada Temperature')

fig = {'data': data, 'layout': my_layout}
offline.plot(fig, filename='Temperatures in CA.html')

# Question 1B.
print('Question 1B\n')
#Using Scattergeo, plot the current humidity in the aforementioned cities. The plot should have:
# a. Title (do not use the same title I have in the sample image)
# b. Adjust the marker size according to the temperature
# c. Adjust the marker colour according to the temperature (any colour scale you like) d. Add a colour bar to the figure
# e. Don’t forget to specify the unit of measure for the metric
norm = colors.Normalize(vmin=min(current_ts), vmax=max(current_ts))

data = [{
  'type': 'scattergeo',
  'lon': lons,
  'lat': lats,
  'marker': {
    'size': [0.2 * mag for mag in current_ts],
    'color': cm.RdYlBu(norm(current_ts)),
    'colorscale': 'RdYlBu',
    'showscale': True,
    'colorbar': {
      'title': 'Temperature (K)'
    }
  }
}]
my_layout = Layout(title='20 cities in Canada Temperature')

fig = {'data': data, 'layout': my_layout}
offline.plot(fig, filename='Color_bars.html')

# Question 1C.
print('Question 1C\n')
#Using Matplotlib, plot a clustered bar chart for temperature and humidity a. The chart should have a title
# b. You should have a double Y axis, one for temperature and one for humidity c. The Y axes should have a title. Specify the unit of measure
# d. Use different colours for humidity and temperature
# e. Add a label for the metrics
humidities = []
temperatures = []

with open(filename, "r") as file:
  weather_data = json.load(file)
#get temperature, humidity and append
for city_w in weather_data:
  humidity = city_w['main']['humidity']
  temperature = city_w['main']['temp'] - 273.15
  humidities.append(humidity)
  temperatures.append(temperature)

width = 0.5
x = np.arange(len(temperatures))
fig, ax = plt.subplots()

ax1 = ax.bar(x - width / 2, temperatures, width, color='gray', label='A')
ax2 = ax.bar(x + width / 2, humidities, width, color='maroon', label='B')
#define labels and other parameters
ax.set_xlabel('Cities')
ax.set_ylabel('Temperature (°C)', color='r')
ax.set_title('Temperature and Humidity')
ax.set_xticks(x, cities, rotation=90)
ax.legend()
fig.tight_layout()
#show plot
plt.show()

# Question 2
print("Question 2a\n")
#  using Plotly, create a bar plot with the count of each weather description.
# 1. For each of the cities, extract the following information:
for city_w in weather_data:
  city = city_w['name']
  description = city_w["weather"][0]["description"]
  print(f"The weather in {city} is described as {description}.")
print("Question 2b\n")
# 2. Create a list of unique description values and their count
# Extracting the weather descriptions from the JSON file
descriptions = []
for city_w in weather_data:
  description = city_w["weather"][0]["description"]
  descriptions.append(description)

# Getting unique description values and their count
unique_descriptions, counts = np.unique(descriptions, return_counts=True)

# Print the results
for description, count in zip(unique_descriptions, counts):
  print(f"{description}: {count}")
print("Question 2c\n")
# Plot the bar chart. The X-axis should have the weather descriptions, while the Y-axis should have the count.
# a. Add a title to the chart
# b. Add a title for the Y-axis

# Plots the bar chart
fig, ax = plt.subplots()

x = np.arange(len(unique_descriptions))
ax.bar(x, counts, align='center')

ax.set_xticks(x)
ax.set_xticklabels(unique_descriptions, rotation=90)
ax.set_title('Weather Descriptions')
ax.set_ylabel('Count')

plt.show()

print("Question 3\n")
# from the given list of cities, extract and print the cities with the most wind speed as well as the least wind speed. Don’t forget to print out the wind speeds for both of them as well.

# Initialize empty lists to store weather data for each city
weather_data = []
wind_speeds = []

# Loop through each city
for city in cities:
  # Constructing the API URL
  url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&appid={my_api}&units=metric"

  # Making the API call
  response = requests.get(url)

  # Checking if the API call was successful
  try:
    response.status_code == 200
    # Store the weather data for the city in the list
    weather_data.append(response.json())

    # Extract the wind speed for the city and append it to the list
    wind_speeds.append(response.json()['wind']['speed'])
  except:
    # Print an error message if the API call failed
    print(f"Unable to retrieve weather data for {city}")

# Find the city with the maximum wind speed
max_wind_speed = max(wind_speeds)
max_wind_speed_city = ""
for city_w in weather_data:
  if city_w['wind']['speed'] == max_wind_speed:
    max_wind_speed_city = city_w['name']
    break

# Find the city with the minimum wind speed
min_wind_speed = min(wind_speeds)
min_wind_speed_city = ""
for city_w in weather_data:
  if city_w['wind']['speed'] == min_wind_speed:
    min_wind_speed_city = city_w['name']
    break

# Print the results
print(
  f"The city with the maximum wind speed is {max_wind_speed_city} with a wind speed of {max_wind_speed} m/s."
)
print(
  f"The city with the minimum wind speed is {min_wind_speed_city} with a wind speed of {min_wind_speed} m/s.\n"
)

print("Question 4")
#  for the list of the cities, using data.json, for each city do the following:
# 1. Extract the sunrise value and store it inside a variable.
# 2. Extract the sunset value and store it inside another variable. Both these values are in a format known as a UNIX timestamp.
# 3. Store their difference (which would be the duration of sunlight on that day) in another variable. Following that, using the utcfromtimestamp() method of the datetime module (documentation:
# https://docs.python.org/3/library/datetime.html#datetime.datetime.utcfromtimestamp), convert the timestamp of the difference variable.
# 4. Once you have the utc time, convert it into a string of the following format - HH:MM using the strftime() method (documentation: https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior), exclude all other elements like day, month, year and seconds.
# 5. Store all the duration strings into a list called as ‘sundurations’.
# 6. Print out the duration of sunlight for each of the cities.

# Read data from the JSON file
with open(filename, "r") as file:
  weather_data = json.load(file)

# Initialize an empty list to store duration of sunlight for each city
sun_durations = []

# Loop through each city
for city_w in weather_data:
  # Extract the sunrise and sunset values from the weather data for the city
  sunrisets = city_w['sys']['sunrise']
  sunset_ts = city_w['sys']['sunset']

  # Calculate the duration of sunlight for the city
  duration_ts = sunset_ts - sunrisets

  # Convert the duration from timestamp to datetime object
  duration_utc = datetime.datetime.utcfromtimestamp(duration_ts)

  # Format the duration as HH:MM string
  duration_str = duration_utc.strftime('%H:%M')

  # Append the duration string to the list
  sun_durations.append(duration_str)

  # Print the duration of sunlight for the city
  print(
    f"The duration of sunlight in {city_w['name']}: {duration_str} hours\n")


# Define a function to calculate the average duration of sunlight
def avgtimes(timestringlist):
  seconds = 0
  for time_str in timestringlist:
    time_parts = time_str.split(':')
    seconds += int(time_parts[0]) * 3600 + int(time_parts[1]) * 60
  avg_seconds = seconds // len(timestringlist)
  avg_hours = avg_seconds // 3600
  avg_minutes = (avg_seconds % 3600) // 60
  return f"{avg_hours:02}:{avg_minutes:02}"


# Calculate the average duration of sunlight for all 20 cities
avg_duration = avgtimes(sun_durations)
print(
  f"The average duration of sunlight in all cities is {avg_duration} hours\n")

print("Question 5")
# for the each city, using data.json:
# 1. Extract the actual temperature from the dictionary as well as the feels like temperature and calculate the difference between those values.
# 2. Following that, print out the name of the city and the difference between the actual temperature and feels like values.

with open("data.json", "r") as file:
  weather_data = json.load(file)

for city_w in weather_data:
  city = city_w['name']
  actual_temp = city_w['main']['temp']
  feels_like_temp = city_w['main']['feels_like']
  temp_diff = actual_temp - feels_like_temp
  print(
    f"The difference between the actual temperature and feels like for {city}: {temp_diff} degrees\n"
  )

#Answer the question: do you think there is a significant difference between the actual temperature compared to the feels-like temperature? Why do you think that may be?
print(
  "\nThere is a significant difference between the actual temperature and the feels-like temperature, this can be as a result of the individual city and the current weather conditions including factors like humidity, wind, and other meteorological factors, which can make the temperature feel different from the actual temperature.\n"
)

print("Question 6")
# 1. Select any city from the list of cities mentioned above.
# 2. Using data.json, get the weather data for the city of your choice and store it in a dictionary.
# 3. From that dictionary, extract the wind speed.
# 4. After that, create a gauge chart (https://plotly.com/python/gauge-charts/).

# Load the weather data from data.json
with open(filename, "r") as file:
  weather_data = json.load(file)

# Select the city of Vancouver
city_data = [data for data in weather_data if data["name"] == "Vancouver"][0]

# Extract the wind speed
wind_speed = city_data["wind"]["speed"]

# Create a gauge chart to display the wind speed
data = [
  go.Indicator(mode="gauge+number",
               value=wind_speed,
               title={"text": "Wind Speed (m/s)"},
               gauge={
                 "axis": {
                   "range": [None, 20]
                 },
                 "bar": {
                   "color": "maroon"
                 },
                 "steps": [{
                   "range": [0, 5],
                   "color": "lightpink"
                 }, {
                   "range": [5, 10],
                   "color": "red"
                 }, {
                   "range": [10, 15],
                   "color": "maroon"
                 }, {
                   "range": [15, 20],
                   "color": "black"
                 }]
               })
]

layout = go.Layout(title="Vancouver Wind Speed")

fig = go.Figure(data=data, layout=layout)

offline.plot(fig, filename="V_windspeed.html")
