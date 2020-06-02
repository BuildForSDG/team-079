import logging


class Config:
    LOGGER_FILE = "logs.log"
    LOG_FORMAT = "%(levelname)s %(asctime)s: %(message)s"
    MAP_API_KEY = 'AIzaSyBr427Ow25KCsgHcHQe_J1V1L39nTouIfk'
    MAX_PLACES = 4
    MAP_NEARBY_SEARCH = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    MAP_PLACE_DETAIL = 'https://maps.googleapis.com/maps/api/place/details/json'
    RESPONDER_LOCATION = 'responder'
    REPORTER_LOCATION = 'reporter'

    # different statuses for reported incidents
    STATUS_PENDING = "PENDING"
    STATUS_AWAIT = "AWAITING RESPONDER"
    STATUS_RESOLVED = "RESOLVED"

    # incident report config params
    ANONYMOUS_USER_ID = 2
    UNCATEGORIZED_REPORT_ID = 1

    # twilio setup
    ACCOUNT_SID = 'AC4d00d14a8f0c3ae0bff3ec2353c6acfe'
    AUTH_TOKEN = 'ec2aac4280cc136dc338137bef3fe0d7'
    FROM_NUMBER = '+12092314443'
    TO_NUMBER = '+2348160016793'


class DevConfig(Config):
    LOG_LEVEL = logging.DEBUG
