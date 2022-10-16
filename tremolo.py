import logging

from quart import Quart, render_template
from quart_cors import cors

log_level: int = logging.INFO
log_format: str = "%(asctime)-15s %(levelname)-8s %(message)s"
log = logging.getLogger(__name__)
log.setLevel(log_level)
log.propagate = False
formatter = logging.Formatter(log_format)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
log.addHandler(handler)

app = Quart(__name__)
app = cors(app)


@app.route('/')
async def index():
    return await render_template('index.html')
