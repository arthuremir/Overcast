import os
from configparser import ConfigParser

keys_cfg = ConfigParser()
keys_cfg.read('keys.cfg')
keys = keys_cfg['Keys']

OWM_TOKEN = keys['OWM']
MAPBOX_TOKEN = keys['MAPBOX']

main_cfg = ConfigParser()
main_cfg.read('main_config.cfg')

SUBSCRIPTION_TYPE = main_cfg['OWM']['subscription_type']
PLT_FIGSIZE = tuple(int(dim) for dim in main_cfg['PLT']['figsize'].split(','))
DPI = int(main_cfg['PLT']['dpi'])

ZOOM = int(main_cfg['MAPBOX']['zoom'])
INIT_COORD = tuple(float(dim) for dim in main_cfg['MAPBOX']['init_coord'].split(','))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or keys['SECRET_KEY']
