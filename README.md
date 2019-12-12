# record-and-replay-proxy

Record and replay http request plugin for [mitmproxy](https://mitmproxy.org/).

![image](https://raw.githubusercontent.com/Chanmoro/record-and-replay-proxy/master/docs/record-and-replay-proxy.png)

# How to use
## Record

```bash
$ docker run -it --rm -p 8080:8080 -v ${PWD}/response_data:/app/response_data chanmoro/record-and-replay-proxy record
```

## Replay

```bash
$ docker run -it --rm -p 8080:8080 -v ${PWD}/response_data:/app/response_data chanmoro/record-and-replay-proxy replay
```

## Setting
Recorded http response is saved into `/app/response_data` by default.  
You can modify save destination dir by setting an environment variable `RESPONSE_DATA_DIR`.

# Example
## Using with curl
Specify http proxy with `-x` option.

```bash
$ curl -k -x localhost:8080 https://github.com/
```

# Development
## Docker build

```bash
$ docker build -t record-and-replay-proxy .
```

## Test

Execute test by pytest.

```bash
$ pytest
```
