import json

from core.util import logger


def pretty_json(jData):
    logger.trace("pretty_json ...")
    logger.trace("The json contains {0} properties".format(len(jData)))
    return json.dumps(jData, indent=4, sort_keys=True)
