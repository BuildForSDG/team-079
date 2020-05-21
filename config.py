import logging


class Config:
    LOGGER_FILE = "logs.log"
    LOG_FORMAT = "%(levelname)s %(asctime)s: %(message)s"
    MAP_API_KEY = 'AIzaSyBr427Ow25KCsgHcHQe_J1V1L39nTouIfk'
    MAX_PLACES = 5
    MAP_NEARBY_SEARCH = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    MAP_PLACE_DETAIL = 'https://maps.googleapis.com/maps/api/place/details/json'


class DevConfig(Config):
    LOG_LEVEL = logging.DEBUG
