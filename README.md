# record-and-replay-proxy

このプロキシを利用すると API や外部サービスへの HTTP レスポンスの記録と、記録したレスポンスをサービスにアクセスせずプロキシから返すことができます

# 使い方

## Setup
### docker ビルド

```bash
$ docker build -t record-and-replay-proxy .
```
## Record & Replay
### レスポンスの record

```bash
$ docker run -it --rm -p 8080:8080 -v ${PWD}/response_data:/app/response_data record-and-replay-proxy /app/record.sh
```

### レスポンスの replay

```bash
$ docker run -it --rm -p 8080:8080 -v ${PWD}/response_data:/app/response_data record-and-replay-proxy /app/replay.sh
```

### 設定
レスポンスデータは `/app/response_data` に保存、ロードされます  
このパスは環境変数 `RESPONSE_DATA_DIR` を設定することで任意のパスに変更できます

### 確認方法

```bash
$ curl -k -x localhost:8080 https://www.doorkeeper.jp/
```

curl の `-x` オプションでプロキシを設定できます

## Test

テストは pytest で書かれています

```bash
$ pytest
```