import os
import urllib.parse

from response_recorder import HttpRequest, HttpResponse, ResponseRecorder


def test_save_and_load_response(tmpdir):
    os.environ['RESPONSE_DATA_PATH'] = tmpdir.strpath
    request = HttpRequest(
        method='GET',
        url='https://hoge.fuga/piyo?k=v&k2=v2'
    )
    response = HttpResponse(
        status=200,
        headers=[(b'Header1', b'Value1'), (b'Header2', b'Value2')],
        body=b'This is response body'
    )
    # レスポンス保存のテスト
    ResponseRecorder.save_response(request, response)
    # <保存先dir>/<リクエストURL>/<HTTPメソッド> のパスにデータが保存されるか
    data_dir = tmpdir.join(urllib.parse.quote_plus(request.url)).join(request.method)
    assert len(data_dir.listdir()) == 3
    assert data_dir.join('metadata').check(file=1)
    assert data_dir.join('response_header').check(file=1)
    assert data_dir.join('response_body').check(file=1)

    # 保存されたレスポンスがロードできるかをテスト
    stub_response = ResponseRecorder.load_response(request)
    assert stub_response.status == 200
    assert stub_response.headers == [(b'Header1', b'Value1'), (b'Header2', b'Value2')]
    assert stub_response.body == b'This is response body'
