#!/usr/bin/env python
import sys
from StateController import StateController
import logging.config


def main():
    state_controller = StateController()
    state_controller.run()


if __name__ == "__main__":
    logging.config.fileConfig('./logging.conf')
    logger = logging.getLogger(__name__)
    logger.info('==================== The program starts ! ==================== ')

    try:
        main()
    except Exception as e:
        logger.error('Error has occurred !!!', exc_info=True)
    else:
        logger.info('==================== The program ended normally ! ==================== ')


