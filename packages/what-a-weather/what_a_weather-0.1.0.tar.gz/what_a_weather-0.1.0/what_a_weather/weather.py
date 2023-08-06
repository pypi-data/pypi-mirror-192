"""
This module uses OPENWEATHERMAP API to generate next 12 hours weather
forecasts.
"""
import requests


class WhatAWeather:
    """Creates a weather object getting en apikey as input
    and either a city name or lat and lon coordinates.
    Package use example:
    # Create a weather object using a city name:
    # The api key below is not guaranteed  to work.
    # get your own apikey from https://openweather.org
    # And wait a couple of hours for the apikey to be activated.

    >>> weather1 = WhatAWeather(api_key="API_KEY", city="Ankara")

    # Using latitude and longitude coordinates
    >>> weather2 = WhatAWeather(api_key="API_KEY", lan=41.1, lon=-4.1)

    # Get complete weather data for the next 12 hours:
    >>> weather1.next_12h()

    # Simplified data for the next 12 hours:
    >>> weather1.next_12h_simplified()

    Sample url to get sky condition icons:
    https://openweathermap.org/img/wn/10d@2x.png
    """

    def __init__(self, api_key, city=None, lat=None, lon=None, units="metric"):
        if lat is not None and lon is not None:
            url = f"https://api.openweathermap.org/data/2.5/forecast" \
                  f"?lat={lat}&lon={lon}&appid={api_key}&units={units}"
            response = requests.get(url)
            self.data = response.json()
        elif city is not None:
            url = f"https://api.openweathermap.org/data/2.5/forecast" \
                  f"?q={city}&appid={api_key}&units={units}"
            response = requests.get(url)
            self.data = response.json()
        else:
            raise TypeError("provide either a city or lan and lon arguments.")

        self._is_status_200()

    def next_12h(self) -> dict:
        """Returns 3-hour data for the next 12 hours as a dict"""
        return self.data["list"][:4]  # 3h period * 4 12h data

    def next_12h_simplified(self) -> list[tuple]:
        """Returns date, temperature and sky conditions every 3 hours
        for next 12 hours as a list of tuple."""
        simple_data = []
        for dict_item in self.data["list"][:4]:
            simple_data.append(
                (dict_item["dt_txt"],
                 dict_item["main"]["temp"],
                 dict_item["weather"][0]["description"],
                 dict_item["weather"][0]["icon"])
            )

        return simple_data

    def _is_status_200(self):
        """Checks API response code and if the code different
        from "200" raises Value error with message from API"""
        if self.data["cod"] != "200":
            raise ValueError(self.data["message"])
