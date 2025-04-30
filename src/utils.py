import json
from flask import Response
from functools import wraps
from datetime import datetime, timezone
import time


def jjsonify(data, status=200):
    response_json = json.dumps(data, ensure_ascii=False, sort_keys=False)
    return Response(response_json, status=status, mimetype="application/json")

def with_execution_time(handler):
    @wraps(handler)
    def wrapper(*args, **kwargs):
        start = time.time()
        body = handler(*args, **kwargs)
        end = time.time()

        elapsed = round((end - start) * 1000, 2)

        response = {
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "execution_time_ms": elapsed
        }

        if isinstance(body, dict):
            response.update(body)
            return jjsonify(response)

        return body

    return wrapper