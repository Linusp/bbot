# -*- coding: utf-8 -*-
import json
from os import getenv
from os.path import join
from flask import Flask, jsonify, request

from utils import decode_to_unicode


class BearyBot(object):
    """A Outgoing Robot for BearyChat"""

    _CONF_FILE = join(getenv('HOME'), '.botrc')

    def __init__(self, trigger_word, controller):
        """初始化操作

        :type trigger_word: str
        :param trigger_word: 在 BearyChat 的机器人管理页面中为 Outgoing
                             机器人设置的触发词

        :type controller: Controller
        :param controller: Outgoing 机器人的中心控制模块，包含了预处理、
                           命令响应和后处理三个模块
        """
        self._trigger_word = decode_to_unicode(trigger_word)
        self._config = {}
        self.read_config()
        self._controller = controller
        self._app = Flask(__name__.split('.')[0])
        self._app.config.update(DEBUG=True)

        self._app.add_url_rule('/', view_func=self.proc, methods=['POST'])

    def read_config(self, conf_file=_CONF_FILE):
        """从 HOME 目录下的配置文件中读取额外的配置"""
        config = {}
        try:
            f = open(conf_file, 'r')
            config = json.load(f)
        except IOError as e:
            print 'failed to read configure'
            print str(e)

        self._config.update(config)

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
