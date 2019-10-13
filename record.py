import os

from mitmproxy import http

from response_recorder import ResponseRecorder


def response(flow: http.HTTPFlow) -> None:
    """ レスポンスをファイルへ保存する """
    ResponseRecorder.save_response(flow.request, flow.response, os.environ['RESPONSE_DATA_PATH'])
