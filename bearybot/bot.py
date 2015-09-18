# -*- coding: utf-8 -*-
import json
from flask import Flask, jsonify, request


class BearyBot(object):
    def __init__(self, trigger_word, controller):
        self._trigger_word = trigger_word
        self._controller = controller
        self._app = Flask(__name__.split('.')[0])
        self._app.config.update(DEBUG=True)

        self._app.add_url_rule('/', view_func=self.proc, methods=['POST'])

    def proc(self):
        print 'request data is %r' % request.data
        try:
            info = json.loads(request.data)
        except Exception:
            print request.data

        result = self._controller.process(info.get('text', ''), info)

        return jsonify(result)

    def run(self, host='0.0.0.0', port=7428):
        self._app.run(host=host, port=port)
