"""Module that contains all background services for managing responses."""
from setup import logger
from background_task import background


@background(schedule=5)
def call_responders():
    logger.info("Calling responders that have not responded at the interval of 2 minutes")
