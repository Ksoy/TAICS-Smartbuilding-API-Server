import logging
import random

from datetime import datetime

from flask import Blueprint, request

from ..db import models
from ..exceptions import InvalidParameterError, TaicsException
from ..utils import response_decorator

devices_app = Blueprint('devices', __name__)
logger = logging.getLogger(__name__)


@devices_app.route('/', methods=['GET'], endpoint='list')
@response_decorator
def devices_list():
    device_records = models.Device.query.all()

    return {
        'kind': 'Collection',
        'devices': [d.export() for d in device_records],
    }


@devices_app.route('/<string:device_ids>/value', methods=['GET'], endpoint='get')
@response_decorator
def devices_get_value(device_ids: str):
    devices = extract_devices(device_ids)

    return {
        'kind': 'Device',
        'devices': [d.export_values() for d in devices],
    }


@devices_app.route('/<string:device_ids>/value', methods=['POST'], endpoint='post')
@response_decorator
def devices_post_value(device_ids: str):
    ids = list(map(lambda x: x.strip(), device_ids.split(',')))

    for d in request.json.get('devices', {}):
        id = d.get('ID')
        if not id or id not in ids:
            raise TaicsException([
                InvalidParameterError(f'{id} is inconsistent')
            ])


        device_record = models.Device.query.filter_by(ID=id).first()
        if not device_record:
            raise TaicsException([
                InvalidParameterError(f'{id} not found')
            ])

        for shortName, value in d.get('values', {}).items():
            logger.info(f'{id}.{shortName}: {value}')

    return request.json


def extract_devices(device_ids: str):
    devices = []
    for id in list(map(lambda x: x.strip(), device_ids.split(','))):
        device_record = models.Device.query.filter_by(ID=id).first()
        if not device_record:
            raise TaicsException([
                InvalidParameterError(f'{id} not found')
            ])
        devices.append(device_record)

    return devices
