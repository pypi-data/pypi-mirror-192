from http import HTTPStatus

import requests
from vulcan.core.utils import logger
from fastapi import HTTPException
from requests.exceptions import HTTPError

GET = "get"
POST = "post"

DEFAULT_ITEMS_PER_PAGE = 30
DEFAULT_ITEMS_SKIP = 0


def http_raise_error(status_code: HTTPStatus, *error_nessage):
    logger.error(*error_nessage)
    raise HTTPException(status_code=status_code, detail=str(error_nessage))


def call(url, method, data):
    try:
        if method == GET:
            response = requests.get(url, data=data)
        elif method == POST:
            response = requests.post(url, data=data)
        else:
            http_raise_error("method ", method, " not implemented yet")

        logger.trace("response", response)

        if response.ok:
            jData = json.loads(response.content)

            return jData, response
        else:
            logger.error(response)
            http_raise_error(response, url, method, data)
    except Exception as error:  # work on python 3.x
        logger.error("Failed on http call: " + str(error))
        http_raise_error(error, url, method, data)
