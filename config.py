import logging


class Config:
    LOGGER_FILE = "logs.log"
    LOG_FORMAT = "%(levelname)s %(asctime)s: %(message)s"
    MAP_API_KEY = 'AIzaSyCSp-f-_FWHw8jfNFF9yd7mgUxaX-DZo8g'
    MAX_PLACES = 5
    MAP_NEARBY_SEARCH = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    MAP_PLACE_DETAIL = 'https://maps.googleapis.com/maps/api/place/details/json'
    RESPONDER_LOCATION = 'responder'
    REPORTER_LOCATION = 'reporter'


class DevConfig(Config):
    LOG_LEVEL = logging.DEBUG
