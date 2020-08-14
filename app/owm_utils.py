import json

from datetime import datetime, timedelta

from config import OWM_TOKEN, SUBSCRIPTION_TYPE
from app.plot_utils import make_plot
from app.clothing_rec import temp_rec, condition_rec

from pyowm.owm import OWM
from pyowm.utils.config import get_default_config_for_subscription_type

from app.utils import to_celsius, prep_location_str, format_time

owm_config_dict = get_default_config_for_subscription_type(SUBSCRIPTION_TYPE)
owm = OWM(OWM_TOKEN, owm_config_dict)
mgr = owm.weather_manager()
reg = owm.city_id_registry()

with open("app/cn2cc.json", "r") as cn2cc:
    cn2cc = json.load(cn2cc)


class WeatherWrapper:
    def __init__(self, lat=None, lon=None, location=None, scale='celsius'):
        if location is not None:
            self.location = location
            if ',' in self.location:
                self.city, self.country = [prep_location_str(loc) for loc in self.location.split(',')]

                if len(self.country) != 2:
                    if self.country in cn2cc:
                        self.country = cn2cc[self.country]
                    else:
                        raise Exception

                list_of_locations = reg.locations_for(city_name=self.city, country=self.country.upper())
            else:
                self.city = prep_location_str(self.location)
                self.country = None

                list_of_locations = reg.locations_for(city_name=self.location)

            if len(list_of_locations) == 0:
                raise Exception

            city_obj = list_of_locations[0]
            self.lat = city_obj.lat
            self.lon = city_obj.lon
        else:
            self.lat = lat
            self.lon = lon
            self.city = None
            self.country = None

        self.current_temperature = None
        self.scale = scale

        self.weather_observation = None
        self.forecast_observation = None
        self.forecast_dict = dict()
        self.forecast_parsed = dict()

    def get_temperature(self):
        self.weather_observation = mgr.weather_at_coords(self.lat, self.lon)
        weather = self.weather_observation.weather
        self.current_temperature = int(round(weather.temperature(self.scale)['temp']))
        return self.current_temperature

    def get_temperature_forecast(self, period='3h'):
        self.forecast_observation = mgr.forecast_at_coords(self.lat, self.lon, period)
        self.forecast_dict = self.forecast_observation.forecast.to_dict()

        self.forecast_parsed = self.get_forecast_dict()
        return self.forecast_parsed

    def save_plot(self):

        time_list = [format_time(t) for t in self.forecast_parsed.keys()]
        temp_list = [temp for temp, _, _ in self.forecast_parsed.values()]

        plot_path = make_plot(time_list, temp_list)

        return plot_path

    def get_forecast_dict(self):
        return {forecast['reference_time']:
                    [to_celsius(forecast['temperature']['temp'], -1),
                     to_celsius(forecast['temperature']['feels_like']),
                     forecast['status']
                     ]
                for forecast in self.forecast_dict['weathers']}

    def get_clothes_rec(self):

        obs = self.select_observations()

        temp_feels_list = [observation[1] for observation in obs]
        conditions_list = [observation[2] for observation in obs]

        average_temp_feels = sum(temp_feels_list) / len(temp_feels_list)

        rec = temp_rec(average_temp_feels) + '\n' + condition_rec(conditions_list)

        return rec

    def select_observations(self):
        if datetime.now().hour < 21:
            req_day = datetime.now().day
        else:
            tom = datetime.now() + timedelta(days=1)
            req_day = tom.day

        obs = list()

        for time, key in self.forecast_parsed.items():
            date = datetime.fromtimestamp(time)
            if date.day == req_day and date.hour >= 6:
                obs.append(key)

        return obs

    def get_icon(self):
        return self.weather_observation.weather.weather_icon_url()

    def location_repr(self):
        if self.city is not None:
            rep_loc = self.city
            if self.country is not None:
                rep_loc += ', ' + self.country
        else:
            rep_loc = 'lat: {}, lon: {}'.format(str(round(self.lat)), str(round(self.lon)))

        return rep_loc
