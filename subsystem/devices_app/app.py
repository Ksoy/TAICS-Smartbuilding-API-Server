import logging
import random

from datetime import datetime

from flask import Blueprint, request
from pytz import timezone

from ..db import models
from ..utils import ntp_decorator

devices_app = Blueprint('devices', __name__)
logger = logging.getLogger(__name__)


@devices_app.route('/', methods=['GET'], endpoint='list')
@ntp_decorator
def devices_list():
    device_records = models.Device.query.all()

    return {
        'self': request.url,
        'kind': 'Collection',
        'timestamp': datetime.now(timezone('Asia/Taipei')).isoformat(),
        'devices': [d.export() for d in device_records],
    }


@devices_app.route('/<string:device_ids>/value', methods=['GET'], endpoint='get')
@ntp_decorator
def devices_get_value(device_ids):
    return {'value': random.random()}


@devices_app.route('/<string:device_ids>/value', methods=['POST'], endpoint='post')
def devices_post_value(device_ids):
    return device_ids
