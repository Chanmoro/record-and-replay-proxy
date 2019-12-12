from mitmproxy import http

from response_recorder import HttpRequest, HttpResponse, ResponseRecorder


def response(flow: http.HTTPFlow) -> None:
    """ レスポンスをファイルへ保存する """
    request = HttpRequest(
        method=flow.request.method,
        url=flow.request.url
    )
    response = HttpResponse(
        status=flow.response.status_code,
        headers=((k, v) for k, v in flow.response.headers.fields),
        body=flow.response.raw_content
    )
    ResponseRecorder.save_response(
        request,
        response)
