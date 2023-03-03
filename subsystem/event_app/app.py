import logging

from datetime import datetime
from multiprocessing import Process
from urllib.parse import urljoin

import requests
import validators

from flask import Blueprint, request
from pytz import timezone

from ..utils import response_decorator

event_app = Blueprint('event', __name__)
logger = logging.getLogger(__name__)


@event_app.route('/trigger', methods=['POST'], endpoint='post')
@response_decorator
def event_trigger():
    msihost = request.json.get('msihost', '')

    if not validators.url(msihost):
        return {
            'kind': 'Error',
            'errors': [
                {
                    'code': 'INVALID_PARAMETER',
                    'message': 'msihost is not valid',
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
        print('Receive event trigger, send requests.')
        res = requests.post(urljoin(self.msihost, 'event'), json={
            'kind': 'Event',
            'self': '',
            'timestamp': datetime.now(timezone('Asia/Taipei')).isoformat(),
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
                    'msg': 'something wrong',
                },
            ],
        })

        if res.status_code != 200:
            print(res.text)
