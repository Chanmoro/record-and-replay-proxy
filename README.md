# record-and-replay-proxy

このプロキシを利用すると API や外部サービスへの HTTP レスポンスの記録と、記録したレスポンスをサービスにアクセスせずプロキシから返すことができます

# 使い方

## docker ビルド

```bash
$ docker build -t record-and-replay-proxy .
```

## レスポンスの record

```bash
$ docker run -it --rm -p 8080:8080 record-and-replay-proxy /app/record.sh
```

## レスポンスの replay

```bash
$ docker run -it --rm -p 8080:8080 record-and-replay-proxy /app/replay.sh
```

## 確認方法

```bash
$ curl -k -x localhost:8080 https://www.doorkeeper.jp/
```

curl の `-x` オプションでプロキシを設定できます

## テスト実行

テストは pytest で書かれています

```bash
$ pytest
```