import os

from mitmproxy import http

from response_recorder import ResponseRecorder


def request(flow: http.HTTPFlow) -> None:
    """ 保存済みのファイルからレスポンスを読み込む """
    try:
        flow.response = ResponseRecorder.load_response(flow.request, os.environ['RESPONSE_DATA_PATH'])
    except Exception as e:
        flow.response = http.HTTPResponse.make(
            502,
            f'Error has occered during load respones. error: {e}',
            {})
        print(f'Error has occered during load respones. error: {e}')
        raise e
