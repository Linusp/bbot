# -*- coding: utf-8 -*-

import logging

from component import (
    gif_func,
    image_search,
    talk_func,
    wiki_func,
)
from utils import clever_split, decode_to_unicode


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='bbot.log')


DEFAULT_KEY = '/default'
COMPONENTS = {
    '/gif': gif_func,
    # '/img': image_search,
    '/wiki': wiki_func,
    '/talk': talk_func,
    DEFAULT_KEY: '/talk',
}


class Controller(object):
    """中心控制模块"""

    def __init__(self, components=COMPONENTS):
        """初始化方法

        :type components: dict
        :param components: 默认的命令组件，在 component.py 中实现，
        key 是一个命令词，对应的 value 是一个函数对象，要求每个命
        令词都以 '/' 符号开始。

        需要注意的是，其中可能包含一个特殊的 key — DEFAULT_KEY，用
        来设置无命令词时使用哪个方法进行处理，DEFAULT_KEY 对应的
        value 不是一个函数对象，而是其他命令词中的一个；若 components
        中没有设置 DEFAULT_KEY，在遇到该情况的输入时不作处理
        """
        self._comps = {}
        self._default_cmd = None

        # 注册命令词及对应的处理方法
        for cmd, func in components.iteritems():
            # 略过 DEFAULT_KEY
            if cmd != DEFAULT_KEY:
                self.register(cmd, func)
            else:
                self._default_cmd = components.get(cmd)

        self.set_default(self._default_cmd)

        self.register('/help', self.help)

    def set_default(self, cmd):
        """设置默认命令词

        :type cmd: string begin with slash
        :param cmd: 默认命令词，必须是已注册的命令
        """
        if cmd in self._comps.keys():
            self._default_cmd = cmd
        else:
            self._default_cmd = None

    def pre_process(self, input_str):
        """内部预处理方法，包括简单的数据清洗、分词等操作

        :type input_str: string
        :param input_str: 待处理的中心模块输入，可能包含命令
        词并跟随相应处理方法的参数
        """
        return clever_split(input_str)

    def cmd_interpreter(self, cmd, paras, infos):
        """内部命令解释方法，从已注册的组件中根据命令词
        调用对应的处理方法

        :type cmd: string
        :param cmd: 合法的命令词

        :type paras: string
        :param paras: 命令处理方法的参数

        :type infos: dict
        :param infos: 命令处理方法的额外参数，用于一些使用第三方
        API 的处理方法，可能包含诸如 API key 等用于认证的参数
        """
        if cmd in self._comps.keys():
            return self._comps[cmd](paras, infos)
        else:
            return {'text': 'unsupported command %s' % cmd}

    def post_process(self, res_dict, infos):
        """内部后处理方法，添加一些用户友好的信息

        :type res_dict: dict
        :param res_dict: 待返回的处理结果

        :type infos: dict
        :param infos: 额外参数，其中包含有从 BearyChat 传来的用户、
        频道信息
        """
        text = res_dict.get('text', '')

        user = infos.get('user_name', 'HanMeimei')
        user_ref = '@%s ' % user

        text = user_ref + '\n' + text
        res_dict['text'] = text

        return res_dict

    def register(self, cmd, func):
        """命令注册方法

        :type cmd: string starts with slash
        :param cmd: 命令词，必须以 '/' 开头，否则会被无视

        :type func: function object
        :param func: 命令词对应的处理方法
        """
        if cmd.startswith('/'):
            self._comps[cmd] = func
        else:
            logging.log(logging.WARN, 'bad command %s', cmd)

    def help(self, paras, infos):
        """输出使用帮助"""
        result = ''

        _ = paras
        _ = infos

        # 遍历已注册组件
        for name, func in self._comps.iteritems():
            description = func.__doc__ if func.__doc__ else 'no description'
            description = decode_to_unicode(description)
            if len(name) > 0:
                result += '+ %s: %s\n' % (name, description)

        if self._default_cmd:
            result += decode_to_unicode('不指定命令时，使用 "%s" 命令\n'
                                        % self._default_cmd)
        return {
            'text': result,
        }

    def process(self, text, infos):
        """中心控制模块对外的统一处理方法

        :type text: string
        :param text: 中心控制模块的原始输入，可能包含命令词及对应
        的参数

        :type infos: dict
        :param infos: 包含 BearyChat 传来的用户、频道信息，以及
        从配置文件读取的其他额外配置信息

        返回一个 dict 类型的结果，该结果可以用 flask 中的 jsonify
        方法处理后返回给请求方
        """
        # 分割原始输入得到一个 list
        comps = self.pre_process(text)

        # 检查 list 的长度和其中的第一个元素
        begin_index = 1
        if len(comps) == 0:
            cmd_str = '/help'
        else:
            if comps[0].startswith('/'):
                cmd_str = comps[0]
            elif self._default_cmd:
                cmd_str = self._default_cmd
                begin_index = 0

        paras = ' '.join(comps[begin_index:])
        res = self.cmd_interpreter(cmd_str, paras, infos)
        return self.post_process(res, infos)
