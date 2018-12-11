CODE_NORMAL_PREFIX = '2202'
CODE_SUCCESS = CODE_NORMAL_PREFIX + '00'
CODE_SUCCESS_GET = CODE_NORMAL_PREFIX + '01'
CODE_SUCCESS_ADD = CODE_NORMAL_PREFIX + '02'
CODE_SUCCESS_UPDATE = CODE_NORMAL_PREFIX + '03'
CODE_SUCCESS_UNCHANGE = CODE_NORMAL_PREFIX + '04'
CODE_SUCCESS_DELETE = CODE_NORMAL_PREFIX + '05'


def result_model(code=CODE_SUCCESS, msg='', data=None):
    result = {
        'code': code,
        'msg': msg
    }
    if data:
        result['data'] = data
    return result
