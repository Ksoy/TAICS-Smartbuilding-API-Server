import ntplib

from flask import jsonify

from . import config

ntp_client = ntplib.NTPClient()


def ntp_decorator(f):
    def wrap(*arg, **args):
        if config.IS_TESTING:
            recv_time = get_ntp_tx()

        result = f(*arg, **args)

        if type(result) is dict:
            if config.IS_TESTING:
                result['ntp'] = {
                    'server_recv_time': recv_time,
                    'server_send_time': get_ntp_tx(),
                }

            return jsonify(result)
        return result
    return wrap


def get_ntp_tx() -> str:
    response = ntp_client.request(config.NTP_SERVER, version=3)
    return str(response.tx_time)
