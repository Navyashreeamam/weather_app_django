import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=49da949a09337343a5d21bdd274b1ba9'

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()  # Save the city to the database
        else:
            form = CityForm()  # Show the form if not valid

    form = CityForm()
    cities = City.objects.all()

    weather_data = []

    for city in cities:
        # Make the API request
        response = requests.get(url.format(city.name))

        # Check if the request was successful
        if response.status_code == 200:
            r = response.json()
            
            # Check if the response contains the expected keys
            city_weather = {
                'city': city.name,
                'temperature': r.get('main', {}).get('temp', 'No data available'),
                'description': r.get('weather', [{}])[0].get('description', 'No description available'),
                'icon': r.get('weather', [{}])[0].get('icon', 'No icon available'),
            }

            weather_data.append(city_weather)
        else:
            # Handle failed API response
            weather_data.append({
                'city': city.name,
                'temperature': 'Error fetching data',
                'description': 'Error fetching data',
                'icon': 'No icon available',
            })

    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'weather/weather.html', context)
