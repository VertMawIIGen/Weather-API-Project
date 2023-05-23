import requests
from geopy.geocoders import Nominatim
from geopy.point import Point
import csv

city_dictionary_list = []
base = "https://api.open-meteo.com/v1/forecast?"
extra_link = "&current_weather=true"
response = requests.get("https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current_weather=true")

def list_searcher(search_query, list):
    matching_dictionaries = []
    for dict in list:
        if dict["city"] == search_query or dict["city_ascii"] == search_query:
            matching_dictionaries.append(dict)
    return matching_dictionaries


def weather_obtainer(base, extra_link, dictionary):
    dictionary_output = dictionary
    latitude = dictionary_output.get('lat')
    longitude = dictionary_output.get('lng')
    path = f"latitude={latitude}&longitude={longitude}"
    apiurl = base + path + extra_link
    data = requests.get(apiurl)
    return data.json()

def format_weather_data(api_input, dictionary):
    dictionary_output = dictionary
    city_name = dictionary_output.get('city')
    country_name = dictionary_output.get('country')
    state_name = dictionary_output.get('admin_name')
    data = api_input
    current_weather = data.get("current_weather")
    print()
    print(f"Current weather for {city_name}, {state_name}, {country_name}:")
    for key in current_weather:
        value = current_weather.get(key)
        print("{:^20}|{:^20}".format(key.title(),value))

with open("worldcities.csv", "r", encoding="UTF-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        city_dictionary_list.append(row)

print("Welcome to the weather searcher.")
user_query = input("What city would you like to know the weather of? ")
matching_cities = list_searcher(user_query, city_dictionary_list)
city_found = False
end_search = False
while city_found == False:
    if len(matching_cities) == 0:
        print("There are no cities that match your query.")
        print()
        user_decision = input("Would you like to retry your query? ")
        if user_decision.lower() == "yes":
            print()
            user_query = input("What city would you like to know the weather of? ")
            matching_cities = list_searcher(user_query, city_dictionary_list)
        else:
            print()
            city_found = True
            end_search = True
    else:
        city_found = True
if end_search == True:
    print("Have a good day.")
else:
    if len(matching_cities) > 1:
        print("There are 2 cities under your query.")
        print()
        character = 65
        for index, i in enumerate(matching_cities):
            print(f"{chr(character)}. {i['city']}, {i['admin_name']}, {i['country']}")
            character += 1
        print()
        user_choice = input("Which city are you referring to? ").upper()
        real_index = int(ord(user_choice) - 65)
        matching_cities = matching_cities[real_index]

    weather_information = weather_obtainer(base, extra_link, matching_cities)
    format_weather_data(weather_information, matching_cities)
