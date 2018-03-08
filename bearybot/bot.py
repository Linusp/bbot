# -*- coding: utf-8 -*-
import json
from flask import Flask, jsonify, request


class BearyBot(object):
    """A Outgoing Robot for BearyChat"""

    def __init__(self, trigger_word, controller):
        """初始化操作

        :type trigger_word: str
        :param trigger_word: 在 BearyChat 的机器人管理页面中为 Outgoing
                             机器人设置的触发词

        :type controller: Controller
        :param controller: Outgoing 机器人的中心控制模块，包含了预处理、
                           命令响应和后处理三个模块
        """
        self._trigger_word = trigger_word
        self._config = {}
        self._controller = controller
        self._app = Flask(__name__.split('.')[0])
        self._app.config.update(DEBUG=True)

        self._app.add_url_rule('/', view_func=self.proc, methods=['POST'])

    def proc(self):
        """机器人处理方法"""
        try:
            info = json.loads(request.data)
        except Exception:
            print request.data

        # 从文本中去除触发词
        text = info.get('text', '')
        text = text[len(self._trigger_word):]

        info.update(self._config)
        result = self._controller.process(text, info)

        return jsonify(result)

    def run(self, host='0.0.0.0', port=7428):
        """启动机器人

        :type host: str
        :param host: 需要监听的主机，默认为 0.0.0.0 ，即接收所有请求

        :type port: int
        :param port: 监听的端口，默认为 7428
        """
        self._app.run(host=host, port=port)
