import logging
import random

from datetime import datetime
from multiprocessing import Process
from urllib.parse import urljoin

import requests

from flask import Blueprint, request

from ..db import models
from ..exceptions import InvalidParameterError, TaicsException
from ..utils import response_decorator

event_app = Blueprint('event', __name__)
logger = logging.getLogger(__name__)


@event_app.route('/trigger', methods=['POST'], endpoint='post')
@response_decorator
def event_trigger():
    msihost = request.json.get('msihost')

    if not msihost:
        return {
            'kind': 'Error',
            'errors': [
                {
                    'code': 'INVALID_PARAMETER',
                    'message': 'msihost not given',
                },
            ],
        }

    if not msihost.endswith('/'):
        return {
            'kind': 'Error',
            'errors': [
                {
                    'code': 'INVALID_PARAMETER',
                    'message': 'msihost should end with \'/\'',
                },
            ],
        }

    event_trigger = EventTrigger(msihost)
    event_trigger.start()

    return {
        'kind': 'Event',
        'message': 'Start event announcement.',
    }


class EventTrigger(Process):
    def __init__(self, msihost, *args, **kwargs):
        super(EventTrigger, self).__init__()

        self.msihost = msihost

    def start(self, *args, **kwargs):
        ret = super(EventTrigger, self).start(*args, **kwargs)
        return ret

    def run(self):
        r = request.post(urljoin(self.msihost, 'event'), json={
            'esiID': 'ESI-0001',
            'esiName': 'ESI-system',
            'events': [
                {
                    'ID': 'E-00001',
                    'type': 'User-defined type A',
                    'status': 0,
                    'level': 1,
                    'time': datetime.now(timezone('Asia/Taipei')).isoformat(),
                    'srcID': 'PM-0001',
                },
            ],
        })
