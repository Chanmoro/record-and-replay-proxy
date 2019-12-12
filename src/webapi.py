import threading

from flask import Flask, jsonify, request

from response_recorder import ResponseRecorder

app = Flask('record-and-replay-proxy')


@app.route('/')
def health_check():
    return "OK"


@app.route('/called_responses')
def called_responses():
    return jsonify(ResponseRecorder.called_responses())


@app.route('/all_registered_responses')
def all_prepared_responses():
    return jsonify(ResponseRecorder.all_registered_responses())


@app.route('/not_called_responses')
def not_called_responses():
    return jsonify(ResponseRecorder.not_called_responses())


@app.route('/response_data_dir')
def response_data_dir():
    return jsonify(ResponseRecorder.response_data_dir())


@app.route('/initialize', methods=['POST'])
def initialize():
    request_json = request.get_json()
    ResponseRecorder.initialize(request_json['response_data_dir'])
    return jsonify("ok")


class WebApi:
    def load(self, loader):
        """ WebAPI を起動する """
        t = threading.Thread(target=app.run,
                             kwargs={
                                 'debug': False,
                                 'host': '0.0.0.0',
                                 'port': 3000,
                             })
        t.start()


addons = [WebApi()]
