import os
import time

from dotenv import load_dotenv

import otlp
from sensor import rms_power

load_dotenv("monitor.env")

endpoint = os.environ["OTLP_ENDPOINT"]
instance_id = os.environ["OTLP_INSTANCE_ID"]
api_key = os.environ["OTLP_API_KEY"]

while True:
    try:
        otlp.send(
            endpoint=endpoint,
            instance_id=instance_id,
            api_key=api_key,
            metric="power_watts",
            value=rms_power(),
            attributes={"location": "somewhere"},
        )
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(60)
