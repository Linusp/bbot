# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

_PUNCT_LIST = set([
    u',', u'.', u'!', u'?', u':',
    u';', u'"', u'\'', u'+', u'-',
    u'\(', u'\)', u'\[', u'\]', u'\{',
    u'\}',
    u'，', u'。', u'！', u'？', u'：',
    u'；', u'“', u'”', u'’', u'‘',
    u'「', u'」',
])


def remove_punct(text):
    """去除文本中的标点符号

    :type text: str 或 unicode
    :param text: 需要去除标点的文本

    返回 unicode 类型的、去除了标点的文本
    """
    return re.sub(''.join(_PUNCT_LIST), ' ', text)


def clever_split(text):
    """更智能的字符串分割方法

    对于一般的情况，按空白符号进行分割，但若空白符号被成对的标点包裹，
    则不对其进行分割
    """
    pairs = {
        u'(': u')',
        u'[': u']',
        u'{': u'}',
        u'\'': u'\'',
        u'"': u'"',
        u'“': u'”',
    }

    pair_stack = []

    points = [0]                # points 记录分割点位置
    for i, ch in enumerate(text):
        # 当符号是成对标点中的结束符号且栈顶为对应的开始符号
        # 那么将开始符号出栈
        if ch in pairs.values() and len(pair_stack) > 0 and \
           pairs.get(pair_stack[len(pair_stack) - 1]) == ch:
            pair_stack.pop()
            continue

        # 当符号是成对标点的开始符号时，将其入栈
        if ch in pairs.keys():
            pair_stack.append(ch)
            continue

        # 当栈为空且符号是空白符号时，记位置其为一个分割点
        if ch.isspace() and len(pair_stack) == 0:
            points.append(i)

    points.append(len(text))

    # 按 points 中记录的分割点对文本进行分割
    result = []
    for begin, end in zip(points[:len(points) - 1], points[1:]):
        sub_str = text[begin:end].strip()
        if len(sub_str) > 0:
            result.append(sub_str)

    return result

