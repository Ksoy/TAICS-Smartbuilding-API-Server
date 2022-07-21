import logging
import random

from datetime import datetime

from flask import Blueprint

from ..db import models
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
def devices_get_value(device_ids):
    return {'value': random.random()}


@devices_app.route('/<string:device_ids>/value', methods=['POST'], endpoint='post')
@response_decorator
def devices_post_value(device_ids):
    return device_ids
