# -*- coding: utf-8 -*-
"""

"""
import requests

from utils import clever_split, decode_to_unicode


def cat_func(paras, infos):
    """喵呜"""
    img_url = requests.get('http://thecatapi.com/api/images/get?format=src&type=gif', allow_redirects=False).headers['location']
    return {
        'attachments': [{'images': [{'url': img_url},]},]
    }


def talk_func(paras, infos):
    """来聊天吧"""
    data = {}
    data['key'] = infos.get('talk_api_key', '')
    data['info'] = ' '.join(paras)
    data['userid'] = infos.get('user', 'HanMeimei')
    url = 'http://www.tuling123.com/openapi/api'

    res = requests.get(url, params=data, headers={'Content-type': 'text/html', 'charset': 'utf-8'})

    code = res.get('code', None)
    if code == 100000:     # 纯文本
        answer = res.get('text', 'Aha').replace('<br>', '\n')
    elif code == 305000:   # 列车
        answer = res.get('text', 'Aha').replace('<br>', '\n')
        answer += '\n'
        infos = res.get('list')[0]
        answer += str(infos.get('trainnum')) + ': '
        answer += '%s[%s] -> ' % (str(infos.get('start')), str(infos.get('starttime')))
        answer += '%s[%s]' % (str(infos.get('terminal')), str(infos.get('endtime')))
    elif code == 302000:
        answer = res.get('text', 'Aha').replace('<br>', '\n')
        answer += '\n'
        infos = res.get('list')[0]
        answer += '[%s](%s)' % (infos.get('article'), infos.get('detailurl'))
        answer += '\nsource: %s' % infos.get('source')
    else:
        answer = 'Aha'

    return {
        'text': answer,
    }


class Controller(object):
    """中心控制模块"""

    def __init__(self):
        """"""
        self._comps = {}
        self.register('/cat', cat_func)
        self.register('/talk', talk_func)
        self.register('', talk_func)
        self.register('/help', self.help)

    def input_process(self, input_str):
        return clever_split(input_str)

    def cmd_interpreter(self, cmd, paras, infos):
        if cmd in self._comps.keys():
            return self._comps[cmd](paras, infos)
        else:
            return 'unsupported command %s' % cmd

    def post_process(self, res_str):
        return res_str

    def register(self, cmd, func):
        """"""
        self._comps[cmd] = func

    def help(self, paras, infos):
        """输出使用帮助"""
        result = ''

        for name, func in self._comps.iteritems():
            func_description = func.__doc__ if func.__doc__ else 'no description'
            if len(name) > 0:
                result += '+ %s: %s\n' % (name, decode_to_unicode(func_description))

        result += decode_to_unicode('不指定命令时，使用 /cat 命令\n')
        return {
            'text': result,
        }

    def process(self, text, infos):
        comps = self.input_process(text)

        if len(comps) == 0:
            func = self._comps.get('/help')
        else:
            func = self._comps.get(comps[0], '/help')

        return func(comps[1:], infos)
