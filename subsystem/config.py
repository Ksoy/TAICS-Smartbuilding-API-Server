import os

from distutils.util import strtobool
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

HOST = ''
PORT = ''

SECRET_KEY = ''

DEBUG = False


def read_config(path: str = f'{BASE_DIR}/.env'):
    if not path or not os.path.isfile(path):
        raise OSError('env file not found: {}'.format(path))

    mod = globals()

    load_dotenv(path)

    def set_(name, parser=str):
        if name not in mod:
            raise ('variable `%s` unknown', name)

        mod[name] = parser(os.getenv(name))

    set_('HOST')
    set_('PORT')
    set_('SECRET_KEY')
    set_('DEBUG', strtobool)
