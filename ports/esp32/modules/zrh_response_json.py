import ujson

class ZrhResponseJson:
    def __init__(self) -> None:
        self._message = None
        self._isSuccess = True
        self._data = None

    def success(self, message, data=None):
        self._message = message
        self._data = data
        self._isSuccess = True

    def error(self, message):
        self._message = message
        self._isSuccess = False

    def json(self):
        return ujson.dumps({
            "message": self._message,
            "isSuccess": self._isSuccess,
            "data": self._data
        }).encode()