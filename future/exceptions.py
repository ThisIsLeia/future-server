
class FutureError(Exception):
    """基礎錯誤類"""

    def __init__(self, message="FutureError"):
        super().__init__(message)


class APIError(FutureError):
    """
    :param message: 錯誤的詳細描述
    :param type: 錯誤類型
            - invalid_request_error
            - api_error
            - channel_error
            - card_error
    :param code: 由第三方返回的錯誤碼
    :param param: 發生錯誤返回錯誤的參數名
    """
    status_code = 400
    type = 'invalid_request_error'
    message = ''
    code = '400'

    def __init__(self, msg=None, status=None, payload=None):
        if msg is None:
            msg = self.message
        if status is None:
            status = self.status_code
        self.status_code = status
        self.message = msg
        if payload is None:
            payload = {
                'failure_code': self.code,
                'failure_msg': self.message,
            }
        self.payload = payload
        super(APIError, self).__init__(self.message)

    def to_dict(self):
        return dict(
            type=self.type,
            message=self.message,
            code=self.code,
            payload=self.payload)


class ValidationError(APIError):
    """客戶端錯誤"""
    code = 40001
    message = "參數錯誤"
    type = "invalid_request"
