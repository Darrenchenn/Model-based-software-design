import logging

logger = logging.getLogger('django')


class Error(Exception):
    def __init__(self, message, additional_info=None):
        super().__init__(message)
        self.message = message
        self.additional_info = additional_info

    def __str__(self):
        return self.message

    def new(self):
        return self.message


def new(msg):
    logger.error(msg)
    return msg
