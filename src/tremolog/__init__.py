import logging

log_level: int = logging.DEBUG
log_format: str = "%(asctime)-15s %(levelname)-8s %(message)s"
log = logging.getLogger(__name__)
log.setLevel(log_level)
log.propagate = False
formatter = logging.Formatter(log_format)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
log.addHandler(handler)
