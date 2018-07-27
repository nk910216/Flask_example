class APIResponse(object):
    SUCCESS = 0

    def __init__(self, data):
        self.retValue = {
            "code": self.SUCCESS,
            "message": "",
            "data": data
        }

    def set_data(self, data):
        self.retValue['data'] = data

    def get_json(self):
        return self.retValue


class ErrorResponse(APIResponse):

    def __init__(self, code, message):
        APIResponse.__init__(self, {})
        self.retValue['code'] = code
        self.retValue['message'] =  message
