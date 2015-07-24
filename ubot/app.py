#!/usr/bin/env python
# coding: utf-8

import json
from flask import Flask, jsonify, request
from bot import handle


PORT = 9816

app = Flask(__name__.split('.')[0])
app.config.update(
    DEBUG=True,
    JSONIFY_PRETTYPRINT_REGULAR=False,
)


@app.route('/', methods=['POST',])
def proc():
    info = json.loads(request.data)

    # all these are unicode object
    cmd_str = ' '.join(info.get('text').split()[1:])
    subdomain = info.get('subdomain')
    channel = info.get('channel_name')
    user = info.get('user_name')

    result = handle(cmd_str, subdomain, channel, user)

    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)

