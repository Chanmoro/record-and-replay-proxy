from mitmproxy import http

from response_recorder import HttpRequest, ResponseRecorder


def request(flow: http.HTTPFlow) -> None:
    """ 保存済みのファイルからレスポンスを読み込む """
    try:
        stub_response = ResponseRecorder.load_response(
            HttpRequest(
                method=flow.request.method,
                url=flow.request.url
            ))
        flow.response = http.HTTPResponse.make(
            stub_response.status,
            stub_response.body,
            stub_response.headers)
    except Exception as e:
        flow.response = http.HTTPResponse.make(
            502,
            f'Error has occered during load respones. error: {e}',
            {})
        print(f'Error has occered during load respones. error: {e}')
        raise e
