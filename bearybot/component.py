# -*- coding: utf-8 -*-
"""可连接到中心控制模块的组件

每个组件都要包含一个命令词和一个处理方法
"""

import random
import requests
import giphypop
import wikipedia

from utils import decode_to_unicode

def gif_func(paras, infos):
    """使用 Gighy API 搜索 GIF 图片"""
    _ = infos
    _GIF_CLIENT = giphypop.Giphy()
    try:
        img_url = _GIF_CLIENT.random_gif(paras).media_url
        return {
            'attachments': [{'images': [{'url': img_url},]},]
        }
    except Exception:
        return {
            'text': 'not found'
        }


def image_search(paras, infos):
    """使用 Google API 搜索图片"""
    _ = infos
    _api_url = 'http://ajax.googleapis.com/ajax/services/search/images'
    params = {
        'v': '1.0',
        'rsz': '8',
        'q': decode_to_unicode(paras),
        'start': str(int(random.random() * 10))
    }
    try:
        resp = requests.get(_api_url, params=params)
        data = resp.json()

        img_url = data[u'responseData'][u'results'][0]['unescapedUrl']
        return {
            'attachments': [{'images': [{'url': img_url},]},]
        }
    except Exception:
        return {
            'text': 'not found'
        }


def talk_func(paras, infos):
    """来聊天吧"""
    data = {}
    data['key'] = infos.get('turing_bot_key', '')
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
            answer = decode_to_unicode(summary) + \
                     u'\n候选关键词: %r' % candidates
            return {
                'text': answer,
            }
        else:
            return {
                'text': 'not found',
            }
