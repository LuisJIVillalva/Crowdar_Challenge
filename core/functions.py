import json

import requests

from core.logging_local import log


def run_service(ws_name, method, expected_response=None, body=None, header=None, params=None, files=None):
    log.info(f'[{method}] invocando servicio {ws_name} ')
    method = method.lower()
    if hasattr(requests, method):
        res =  getattr(requests, method)(url=ws_name, json=body, headers=header, params=params, files=files)
        if expected_response is not None:
            assert res.status_code == expected_response, f"Expected status code {expected_response} but got {res.status_code}"
        return res
    else:
        raise ValueError(f"HTTP method '{method}' is not supported.")

def format_json_pretty(json_response):
    return json.dumps(json_response, indent=4, ensure_ascii=False)