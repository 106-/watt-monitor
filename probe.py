import os

from dotenv import load_dotenv

import otlp

load_dotenv("monitor.env")

endpoint = os.environ["OTLP_ENDPOINT"]
instance_id = os.environ["OTLP_INSTANCE_ID"]
api_key = os.environ["OTLP_API_KEY"]

otlp.send(
    endpoint=endpoint,
    instance_id=instance_id,
    api_key=api_key,
    metric="power_watts",
    value=42.0,
    attributes={"location": "somewhere"},
)
print("probe ok: power_watts=42.0")
