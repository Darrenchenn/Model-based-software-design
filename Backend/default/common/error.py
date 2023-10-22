import logging

from django.http import JsonResponse, HttpResponseBadRequest

logger = logging.getLogger('django')


class Error:
    def __init__(self, message):
        self.message = message

    def new(self):
        logger.error(self.message)
        return self.message

    def http_response_new(self):
        logger.error(self.message)
        return HttpResponseBadRequest(JsonResponse({
            "error": self.message,
        }))
