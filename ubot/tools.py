# -*- coding: utf-8 -*-
import re
from os.path import abspath
from IPython import parallel

CLIENT = parallel.Client()[0]


def remove_punct(text):
    """移除标点等无用符号"""
    if isinstance(text, str):
        text = text.decode('utf-8')

    try:
        text = re.sub(u',.!?:;"+-\(\)\[\]\{\}，。；！？“”‘’「」', u" ", text)
    except Exception:
        pass

    return text


def text_clean(text):
    """初步清洗"""
    text = remove_punct(text)
    text = re.sub('\t\n\r', ' ', text)
    return text


def eng_clean(text):
    return re.sub("[^A-Z^a-z^0-9^\s^'^-]", " ", text)


def chi_clean(text):
    return text


def is_chinese_char(uchar):
    """whether a unicode is Chinese"""
    return (uchar >= u'\u4e00' and uchar<=u'\u9fa5') and 1 or 0


def is_chinese(text, bar=0.5):
    if isinstance(text, str):
        text = text.decode("utf8")

    if isinstance(text, unicode):
        L = len(text)
        if not L:
            return False
        return sum([is_chinese_char(ch) for ch in text])/float(L) > bar
    else:
        return False


def is_english(text):
    return not is_chinese(text)


def decode_to_unicode(text):
    if isinstance(text, str):
        return text.decode('utf-8')
    elif isinstance(text, unicode):
        return text
    else:
        raise Exception('Input is neither a string nor a unicode object.')


def encode_from_unicode(text):
    if isinstance(text, str):
        return text
    elif isinstance(text, unicode):
        return text.encode('utf-8')
    else:
        raise Exception('Input is neither a string nor a unicode object.')


def clever_split(text):
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

    points = [0]
    for i, ch in enumerate(text):
        if ch in pairs.values() and len(pair_stack) > 0 and \
           pairs.get(pair_stack[len(pair_stack) - 1]) == ch:
            pair_stack.pop()
            continue

        if ch in pairs.keys():
            pair_stack.append(ch)
            continue

        if ch.isspace() and len(pair_stack) == 0:
            points.append(i)
    points.append(len(text))

    result = []
    for begin, end in zip(points[:len(points) - 1], points[1:]):
        result.append(text[begin:end].strip())

    return result


def run_cell(code):
    # 三种情况
    # 1. 有 print 输出的语句
    # 2. 有返回值的语句
    # 3. 即无返回值也无 print 输出的语句
    # 现在只能得到 1 的结果
    meta = None
    try:
        result = CLIENT.execute(code, block=True)
        meta = result.metadata
    except Exception as e:
        return str(e)

    result_str = ''
    if meta.get('status') == 'ok':
        if meta.get('stdout') != '':
            result_str = meta.get('stdout')
        else:
            result_str = 'ok'
    else:
        result_str = meta.get('status')

    return result_str


if __name__ == '__main__':
    print run_cell('3+3')
