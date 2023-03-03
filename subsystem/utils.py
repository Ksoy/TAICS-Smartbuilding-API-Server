from datetime import datetime

from flask import jsonify, request
from pytz import timezone

from .exceptions import TaicsException


def response_decorator(f):
    def wrap(*arg, **args):
        try:
            result = f(*arg, **args)
        except TaicsException as e:
            result = e.response()

        if type(result) is dict:
            result.update({
                'self': request.url,
                'timestamp': datetime.now(timezone('Asia/Taipei')).isoformat(),
            })

            return jsonify(result)
        return result
    return wrap
