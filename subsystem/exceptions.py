class AbstractError():
    def __init__(self, message=''):
        self.message = message

    def __repr__(self):
        return self.to_dict()

    def to_dict(self):
        raise NotImplementedError()


class InvalidParameterError(AbstractError):
    def to_dict(self):
        return {
            'code': 'INVALID_PARAMETER',
            'message': self.message or '請求參數錯誤',
        }


class TaicsException(Exception):
    def __init__(self, errors: [AbstractError]):
        self.errors = errors

    def response(self) -> dict:
        return {
            "kind": "Error",
            "errors": [e.to_dict() for e in self.errors],
        }

