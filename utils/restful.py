from flask import jsonify


class HttpCode(object):
  ok = 200
  unloginerror = 401
  permissionerror = 403
  paramserror = 400
  servererror = 500


def _restful_result(code, message, data):
  return jsonify({"message": message or "", "data": data or {}}), code


def ok(message=None, data=None):
  return _restful_result(code=HttpCode.ok, message=message, data=data)


def unlogin_error(message="have not logined！"):
  return _restful_result(code=HttpCode.unloginerror, message=message, data=None)


def permission_error(message="have no permission！"):
  return _restful_result(code=HttpCode.paramserror, message=message, data=None)


def params_error(message="argument error！"):
  return _restful_result(code=HttpCode.paramserror, message=message, data=None)


def server_error(message="server is fail！"):
  return _restful_result(code=HttpCode.servererror, message=message or 'server intelnal error', data=None)
