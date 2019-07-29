from typing import Dict, Any

class HttpError:

    code = 0
    msg_short = ''
    msg_long = ''

    def __init__(self, code: int, msg_short: str, msg_long: str):
        self.code = code
        self.msg_short = msg_short
        self.msg_long = msg_long

    @staticmethod
    def error404()->Dict[str, Any]:
        return HttpError(404, 'Oops! This Page Could Not Be Found', 'Sorry but the page you are looking for does not exist, have been removed. name changed or is temporarily unavailable').__dict__

if __name__ == '__main__':
    print(HttpError.error404())