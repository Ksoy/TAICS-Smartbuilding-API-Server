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
            recv_time = get_ntp_tx(config.NTP_SERVER1)

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
                        'ntp_server': [config.NTP_SERVER1, config.NTP_SERVER2],
                        'api_recv_time': recv_time,
                        'api_send_time': get_ntp_tx(config.NTP_SERVER2),
                    }
                })

            return jsonify(result)
        return result
    return wrap


def get_ntp_tx(host) -> str:
    try:
        response = ntp_client.request(host, version=3, timeout=1)
    except ntplib.NTPException:
        return 'Failed to get ntp server time'
    return str(response.tx_time)
