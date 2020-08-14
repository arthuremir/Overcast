import os
import json

from flask import render_template
from flask import request
from pyowm.commons.exceptions import APIRequestError

from app import app
from app.owm_utils import WeatherWrapper

from config import MAPBOX_TOKEN, ZOOM, INIT_COORD


@app.route('/')
def menu_page():
    return render_template('index.html')


@app.route('/map', methods=['GET', 'POST'])
def map_page():
    return render_template('mb.html',
                           MAPBOX_TOKEN=MAPBOX_TOKEN,
                           zoom=ZOOM,
                           lat=INIT_COORD[1],
                           lon=INIT_COORD[0])


@app.route('/forecast')
def forecast_page():
    coords = request.args.get('coords')
    if coords:
        try:
            coords = json.loads(coords)
        except json.decoder.JSONDecodeError:
            return render_template('forecast.html',
                                   error_message='Incorrect request')

        try:
            w = WeatherWrapper(lat=coords['lat'], lon=coords['lng'])
        except Exception:
            return render_template('forecast.html',
                                   error_message='Location not found')

        temperature = w.get_temperature()
        icon_url = w.get_icon()
        w.get_temperature_forecast()
        plot_path = w.save_plot()
        rec = w.get_clothes_rec()

        return render_template('forecast.html',
                               temperature=temperature,
                               mod='C',
                               icon_url=icon_url,
                               location=w.location_repr(),
                               recommendation=rec,
                               plot_path='plots/' + os.path.basename(plot_path))

    else:
        location = request.args.get('location')
        if location:
            try:
                w = WeatherWrapper(location=location)
                temperature = w.get_temperature()
                icon_url = w.get_icon()
                w.get_temperature_forecast()
                plot_path = w.save_plot()
                rec = w.get_clothes_rec()

            except APIRequestError:
                return render_template('forecast.html',
                                       error_message='Incorrect request')
            except Exception:
                return render_template('forecast.html',
                                       error_message='Location not found')

            return render_template('forecast.html',
                                   temperature=temperature,
                                   mod='C',
                                   icon_url=icon_url,
                                   location=w.location_repr(),
                                   recommendation=rec,
                                   plot_path='plots/' + os.path.basename(plot_path))
        else:
            return render_template('forecast.html')
