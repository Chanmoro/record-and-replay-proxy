import glob
import json
import os
import urllib.parse
from dataclasses import asdict, dataclass
from typing import Tuple, Optional, Iterable


class ResponseDataNotFound(Exception):
    """ レスポンスのファイルが存在しない場合の例外 """
    pass


@dataclass(frozen=True)
class RequestMetaData:
    url: str
    method: str
    status: int


@dataclass(frozen=True)
class HttpRequest:
    method: str
    url: str


@dataclass(frozen=True)
class HttpResponse:
    status: int
    headers: Iterable[Tuple[bytes, bytes]]
    body: Optional[bytes]


class FileReaderWriter:
    @classmethod
    def save_to_file(cls, filename: str, byte_data: bytes):
        """
        引数で渡されたbyteデータをファイルに保存する
        :param filename:
        :param byte_data:
        :return:
        """
        with open(filename, 'wb') as f:
            f.write(byte_data)

    @classmethod
    def load_from_file(cls, filename: str) -> bytes:
        """
        ファイルを読み込む
        :param filename:
        :return:
        """
        with open(filename, 'rb') as f:
            return f.read()


class ResponseRecorder:
    CALLED_REQUESTS = []
    RESPONSE_DATA_DIR = os.getenv('RESPONSE_DATA_DIR', './response_data')

    @classmethod
    def initialize(cls, response_data_dir: str):
        cls.CALLED_REQUESTS = []
        cls.RESPONSE_DATA_DIR = response_data_dir

    @classmethod
    def response_data_dir(cls):
        return cls.RESPONSE_DATA_DIR

    @classmethod
    def called_responses(cls):
        return cls.CALLED_REQUESTS

    @classmethod
    def all_registered_responses(cls):
        return glob.glob(f'{cls.RESPONSE_DATA_DIR}/*/*')

    @classmethod
    def not_called_responses(cls):
        return list(set(cls.all_registered_responses()) - set(cls.called_responses()))

    @classmethod
    def load_response(cls, request: HttpRequest) -> HttpResponse:
        """
        保存されたレスポンスをロードする
        :param request:
        :return:
        """
        file_path = cls._get_data_path(request)
        print('==> Response data is loaded from {}'.format(file_path))

        # スタブがロードしようとしたファイルのパスを記録する
        cls.CALLED_REQUESTS.append(file_path)

        # 該当するスタブのファイルがない場合は例外を発生させる
        if not os.path.exists(file_path):
            raise ResponseDataNotFound('There is no such stub data dir. {}'.format(file_path))

        # ファイルをロードして各オブジェクトを復元する
        metadata = RequestMetaData(**json.loads(
            FileReaderWriter.load_from_file('{}/{}'.format(file_path, 'metadata')).decode('UTF-8'),
        ))
        headers = cls._bytes_to_headers(FileReaderWriter.load_from_file('{}/{}'.format(file_path, 'response_header')))
        body = FileReaderWriter.load_from_file('{}/{}'.format(file_path, 'response_body'))

        # Response オブジェクトを作成する
        return HttpResponse(
            status=metadata.status,
            headers=headers,
            body=body
        )

    @classmethod
    def save_response(cls, request: HttpRequest, response: HttpResponse):
        """
        HTTPレスポンスをファイルに保存する
        :param request:
        :param response:
        :return:
        """
        export_path = cls._get_data_path(request)
        print('==> Response data is saved into {}'.format(export_path))

        # 出力先のディレクトリがなければ作成する
        if not os.path.exists(export_path):
            os.makedirs(export_path)

        # メタデータを保存
        metadata = RequestMetaData(
            url=request.url,
            method=request.method,
            status=response.status,
        )
        FileReaderWriter.save_to_file('{}/{}'.format(export_path, 'metadata'),
                                      json.dumps(asdict(metadata), indent=4).encode('UTF-8'))

        # レスポンスヘッダーを保存
        FileReaderWriter.save_to_file('{}/{}'.format(export_path, 'response_header'),
                                      cls._headers_to_bytes(response.headers))

        # レスポンスボディを保存
        body_bytes = response.body
        FileReaderWriter.save_to_file('{}/{}'.format(export_path, 'response_body'), body_bytes)

    @classmethod
    def _get_data_path(cls, request: HttpRequest):
        """ 保存先のパスを生成する """
        file_path = '{}/{}/{}'.format(
            cls.RESPONSE_DATA_DIR,
            urllib.parse.quote_plus(request.url),
            request.method
        )
        return file_path

    @classmethod
    def _headers_to_bytes(cls, headers: Iterable) -> bytes:
        if headers:
            return b"\r\n".join(b": ".join(header) for header in headers) + b"\r\n"
        else:
            return b""

    @classmethod
    def _bytes_to_headers(cls, raw_headers: bytes) -> Iterable:
        return [(l.split(b": ")[0], l.split(b": ")[1]) for l in raw_headers.split(b"\r\n") if l]
