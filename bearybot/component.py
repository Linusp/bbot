# -*- coding: utf-8 -*-
"""可连接到中心控制模块的组件

每个组件都要包含一个命令词和一个处理方法
"""
import os
import json
import requests
import giphypop
import wikipedia


def gif_func(paras, infos):
    """使用 Gighy API 搜索 GIF 图片"""
    _GIF_CLIENT = giphypop.Giphy()
    try:
        img_url = _GIF_CLIENT.random_gif(paras).media_url
        return {
            'attachments': [{'images': [{'url': img_url}, ]}, ]
        }
    except Exception:
        return {
            'text': 'not found'
        }


def talk_func(paras, infos):
    """来聊天吧"""
    data = {}
    data['key'] = os.environ.get('TURING_BOT_KEY', '')
    data['info'] = paras
    data['userid'] = infos.get('user_name', 'HanMeimei')
    url = 'http://www.tuling123.com/openapi/api'

    res = requests.get(url,
                       params=data,
                       headers={'Content-type': 'text/html', 'charset': 'utf-8'})
    res = res.json()

    # code = res.get('code', None)
    answer = res.get('text', 'Aha').replace('<br>', '\n')

    return {
        'text': answer,
    }


def wiki_func(paras, infos):
    """中文维基百科查询"""
    wikipedia.set_lang("zh")
    candidates = wikipedia.search(paras)

    if len(candidates) <= 0:
        return {
            'text': 'not found',
        }
    else:
        summary = None
        for keyword in candidates:
            try:
                summary = wikipedia.summary(keyword, sentences=1)
                break
            except Exception: # 可能发生歧义异常，见 wikipedia 文档
                continue
        if summary:
            answer = summary + u'\n候选关键词: %s' % u', '.join(candidates)
            return {
                'text': answer,
            }
        else:
            return {
                'text': 'not found',
            }


def explain_dict_res(youdao_dict_res):
    """将有道翻译结果组织好返回"""
    res = u''

    _d = youdao_dict_res
    has_result = False

    query = _d['query']

    res += query

    if 'basic' in _d:
        has_result = True
        _b = _d['basic']

        if 'phonetic' in _b:
            res += '[' + _b['phonetic'] + ']\n'
        else:
            res += '\n'

        if 'explains' in _b:
            res += '  Word Explanation:\n'
            res += '\n'.join(
                ['     * ' + explain for explain in _b['explains']]
            )
        else:
            res += '\n'

    elif 'translation' in _d:
        has_result = True
        res += '\n  Translation:\n'
        res += '\n'.join(
            ['     * ' + trans + '\n' for trans in _b['translation']]
        )
    else:
        res += '\n'

    #web reference
    if 'web' in _d:
        has_result = True
        res += '\n  Web Reference:\n'

        web = _d['web'][:3]
        for web_res in web:
            key = web_res['key']
            values = web_res['value']
            res += '     * ' + key + '\n'
            res += '       '
            res += u';'.join(values)
            res += '\n'

    if not has_result:
        res = ' -- No result for this query.'

    return res


def dict_func(paras, info):
    """有道词典查询"""
    key = os.environ.get('YOUDAO_API_KEY')
    key_from = os.environ.get('YOUDAO_KEY_FROM')
    if not key or not key_from:
        return {
            'text': 'robot component error(invalid api key)',
        }

    data = {}
    data['key'] = key
    data['keyfrom'] = key_from
    data['type'] = 'data'
    data['version'] = '1.1'
    data['doctype'] = 'json'
    data['q'] = paras

    r = requests.get('http://fanyi.youdao.com/openapi.do', params=data)
    req = None
    try:
        req = json.loads(r.text)
    except Exception:
        return {
            'text': 'unknown error',
        }

    err_dict = {
        20: u'要翻译的文本过长',
        30: u'无法进行有效的翻译',
        40: u'不支持的语言类型',
        50: u'无效的key',
        60: u'无词典结果',
    }
    err_code = req.get(u'errorCode', 60)
    if err_code in err_dict:
        return {
            'text': err_dict.get(err_code),
        }

    return {
        'text': explain_dict_res(req),
    }
