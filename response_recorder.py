import json
import os
import urllib.parse
from dataclasses import dataclass
from typing import Dict, Optional

from mitmproxy import http
from mitmproxy.net.http import Headers


class ResponseDataNotFound(Exception):
    """ レスポンスのファイルが存在しない場合の例外 """
    pass


@dataclass(frozen=True)
class HttpRequest:
    method: str
    url: str


@dataclass(frozen=True)
class HttpResponse:
    status_code: int
    headers: Dict[str, str]
    body: str


class ResponseRecorder:
    CALLED_REQUESTS = []

    @classmethod
    def load_response(cls, request: http.HTTPRequest, base_path: str) -> http.HTTPResponse:
        """
        保存されたレスポンスをロードする
        :param request:
        :return:
        """
        load_path = cls._get_data_path(request, base_path)
        print('==> Response data is loaded from {}'.format(load_path))

        # スタブがロードしようとしたファイルのパスを記録する
        cls.CALLED_REQUESTS.append(load_path)

        # 該当するスタブのファイルがない場合は例外を発生させる
        if not os.path.exists(load_path):
            raise ResponseDataNotFound('There is no such stub data dir. {}'.format(load_path))

        # ファイルをロードして各オブジェクトを復元する
        metadata = json.loads(cls._load_from_file('{}/{}'.format(load_path, 'metadata')).decode('UTF-8'))
        headers = cls.bytes_to_headers(cls._load_from_file('{}/{}'.format(load_path, 'response_headers')))
        body = cls._load_from_file('{}/{}'.format(load_path, 'response_body'))

        # Response オブジェクトを作成する
        return http.HTTPResponse.make(
            metadata['status'],
            body,
            headers)

    @classmethod
    def headers_to_bytes(cls, headers: Headers) -> bytes:
        return bytes(headers)

    @classmethod
    def bytes_to_headers(cls, raw_headers: bytes) -> list:
        return [(l.split(b": ")[0], l.split(b": ")[1]) for l in raw_headers.split(b"\n") if l]

    @classmethod
    def save_response(cls, request: http.HTTPRequest, response: http.HTTPResponse, base_path: str):
        """
        HTTPレスポンスをファイルに保存する
        :param request:
        :param response:
        :return:
        """
        export_path = cls._get_data_path(request, base_path)
        print('==> Response data is saved into {}'.format(export_path))

        # 出力先のディレクトリがなければ作成する
        if not os.path.exists(export_path):
            os.makedirs(export_path)

        # メタデータを保存
        metadata = {
            'url': request.url,
            'method': request.method,
            'status': response.status_code,
        }
        cls._save_to_file('{}/{}'.format(export_path, 'metadata'),
                          json.dumps(metadata, indent=4).encode('UTF-8'))

        # レスポンスヘッダーを保存
        cls._save_to_file('{}/{}'.format(export_path, 'response_headers'),
                          cls.headers_to_bytes(response.headers))

        # レスポンスボディを保存
        body_bytes = response.content
        cls._save_to_file('{}/{}'.format(export_path, 'response_body'), body_bytes)

    @classmethod
    def _get_data_path(cls, request: http.HTTPRequest, base_path: str):
        """
        保存先のパスを生成する
        :param request:
        :param base_path:
        :return:
        """
        # file_path = './scouty/tests/data/stub_data/{}/{}/{}'.format(
        file_path = '{}/{}/{}'.format(
            base_path,
            urllib.parse.quote_plus(request.url),
            request.method
        )
        return file_path

    @classmethod
    def _save_to_file(cls, filename: str, byte_data: bytes):
        """
        引数で渡されたbyteデータをファイルに保存する
        :param filename:
        :param byte_data:
        :return:
        """
        with open(filename, 'wb') as f:
            f.write(byte_data)

    @classmethod
    def _load_from_file(cls, filename: str) -> Optional[bytes]:
        """
        ファイルを読み込む
        ファイルが存在しない場合はNoneを返却する
        :param filename:
        :return:
        """
        try:
            with open(filename, 'rb') as f:
                byte_data = f.read()
        except FileNotFoundError:
            byte_data = None

        return byte_data
