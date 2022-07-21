import ntplib

from datetime import datetime

from flask import jsonify, request
from pytz import timezone

from . import config
from .exceptions import TaicsException

ntp_client = ntplib.NTPClient()


def response_decorator(f):
    def wrap(*arg, **args):
        if config.IS_TESTING:
            recv_time = get_ntp_tx()

        try:
            result = f(*arg, **args)
        except TaicsException as e:
            result = e.response()

        if type(result) is dict:
            result.update({
                'self': request.url,
                'timestamp': datetime.now(timezone('Asia/Taipei')).isoformat(),
            })

            if config.IS_TESTING:
                result.update({
                    'ntp': {
                        'ntp_server': config.NTP_SERVER,
                        'api_recv_time': recv_time,
                        'api_send_time': get_ntp_tx(),
                    }
                })

            return jsonify(result)
        return result
    return wrap


def get_ntp_tx() -> str:
    response = ntp_client.request(config.NTP_SERVER, version=3)
    return str(response.tx_time)
