import logging

from pythonjsonlogger import jsonlogger

logger = logging.getLogger("oap-rq")
logger.setLevel(logging.INFO)
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter("[%(levelname)8s] %(message)  %(asctime)")
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
lg = logger
