# -*- coding: utf-8 -*-
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


def decode_to_unicode(text):
    """将文本安全地转换为 unicode 串

    :type text: str 或 unicode
    :param text: 需要转换的文本

    如果参数的类型不是 str 也不是 unicode ，将会抛出 TypeError 异常
    """
    if isinstance(text, str):
        return text.decode('utf-8')
    elif isinstance(text, unicode):
        return text
    else:
        raise TypeError('Wrong type %r(should be str or unicode)' % type(text))


def encode_from_unicode(text):
    """将文本安全地转换为 ascii 串

    :type text: str 或 unicode
    :param text: 需要转换的文本

    如果参数的类型不是 str 也不是 unicode ，将会抛出 TypeError 异常
    """
    if isinstance(text, str):
        return text
    elif isinstance(text, unicode):
        return text.encode('utf-8')
    else:
        raise TypeError('Wrong type %r(should be str or unicode)' % type(text))


def remove_punct(text):
    """去除文本中的标点符号

    :type text: str 或 unicode
    :param text: 需要去除标点的文本

    返回 unicode 类型的、去除了标点的文本
    """
    return re.sub(''.join(_PUNCT_LIST), ' ', decode_to_unicode(text))


def clever_split(text):
    """更智能的字符串分割方法

    对于一般的情况，按空白符号进行分割，但若空白符号被成对的标点包裹，
    则不对其进行分割
    """
    text = decode_to_unicode(text)

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
            print pair_stack
            continue

        # 当符号是成对标点的开始符号时，将其入栈
        if ch in pairs.keys():
            pair_stack.append(ch)
            print pair_stack
            continue

        # 当栈为空且符号是空白符号时，记位置其为一个分割点
        if ch.isspace() and len(pair_stack) == 0:
            points.append(i)
            print points

    points.append(len(text))

    # 按 points 中记录的分割点对文本进行分割
    result = []
    for begin, end in zip(points[:len(points) - 1], points[1:]):
        sub_str = text[begin:end].strip()
        if len(sub_str) > 0:
            result.append(sub_str)

    return result

