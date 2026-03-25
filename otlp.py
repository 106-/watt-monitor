"""OTLP/HTTP JSON でメトリクスを Grafana Cloud に送信する。"""

import base64
import time

import requests


def send(
    endpoint: str,
    instance_id: str,
    api_key: str,
    metric: str,
    value: float,
    attributes: dict,
) -> None:
    auth = base64.b64encode(f"{instance_id}:{api_key}".encode()).decode()
    body = {
        "resourceMetrics": [
            {
                "scopeMetrics": [
                    {
                        "metrics": [
                            {
                                "name": metric,
                                "gauge": {
                                    "dataPoints": [
                                        {
                                            "asDouble": value,
                                            "timeUnixNano": int(time.time() * 1e9),
                                            "attributes": [
                                                {"key": k, "value": {"stringValue": v}}
                                                for k, v in attributes.items()
                                            ],
                                        }
                                    ]
                                },
                            }
                        ]
                    }
                ]
            }
        ]
    }
    resp = requests.post(
        endpoint,
        json=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Basic {auth}",
        },
    )
    resp.raise_for_status()
