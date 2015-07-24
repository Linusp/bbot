# -*- coding: utf-8 -*-
import requests
import subprocess
import wikipedia

from bot_mem import bot_memory
from tools import encode_from_unicode, clever_split, run_cell


def usage():
    result = ''
    result += '1. /list : 若不带参数，列出前20个可查询关键词;带参数则查询相关的可用关键词(前10个).\n'
    result += '2. /teach: 插入或更新记录，用法: /teach K:<关键词> D:<描述> T:<标签1>,<标签2>,...\n'
    result += '3. /wiki: 查询维基百科, 用法: /wiki <关键词> L:<语言>.\n'
    result += '4. /cat: 喵呜~\n'
    result += '5. /fortune: 喵呜~\n'
    result += '6. /help: 查看帮助.\n'
    result += '7. /py: 执行 python 语句'
    result += '8. 直接跟随关键词，则进行查询操作.支持批量查询，多个不同的关键词请用空格分隔.'
    return result



def show_list(args):
    result = ''
    res_list = []
    for elem in args:
        if len(res_list) >= 10:
            break

        for res in bot_memory.associate(elem):
            res_list.append(res)
            if len(res_list) >= 10:
                break

    if res_list == [] and args in (None, []):
        for res in bot_memory.associate_all():
            res_list.append(res)
            if len(res_list) >= 20:
                break

    for i, res in enumerate(res_list):
        result += '%d. %s:%s\n' % (i + 1, res[0], res[1])

    return result


def teach(args):
    try:
        obj = None
        description = None
        tags = None
        for elem in args:
            if elem.startswith('K:') and not elem.endswith(':'):
                obj = elem.split(':')[1]
            if elem.startswith('D:') and not elem.endswith(':'):
                description = elem.split(':')[1]
            if elem.startswith('T:') and not elem.endswith(':'):
                tags = elem.split(':')[1].split(',')

        if obj and description and tags:
            bot_memory.update(obj, description, tags)
            return 'Done.'
        else:
            return '使用 /help 查看帮助.'
    except Exception:
        return 'Error.'


def search(args):
    result = ''
    for query in args:
        result += bot_memory.recall(query) + '\n'

    return result


def wiki(args):
    obj = None
    lang = 'en'
    for elem in args:
        if not elem.startswith('L:'):
            obj = elem
        elif not elem.endswith(':'):
            lang = elem.split(':')[1]

    if obj is not None:
        wikipedia.set_lang(lang)
        candidate_list = wikipedia.search(obj)
        if candidate_list in (None, []):
            return 'Not found on Wikipedia.'
        else:
            return wikipedia.summary(candidate_list[0])
    else:
        return '使用 /help 查看帮助.'


def fortune():
    p = subprocess.Popen(['fortune'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result, err = p.communicate()
    return result


def cat(args):
    img_url = requests.get('http://thecatapi.com/api/images/get?format=src&type=gif', allow_redirects=False).headers['location']
    return {
        'attachments': [{'images': [{'url': img_url},]},]
    }


def py_eval(args):
    py_code = ' '.join(args)
    return run_cell(py_code)


def call_command(cmd_str, *args):
    if not cmd_str.startswith('/'):
        return search([cmd_str] + args[0])

    if cmd_str == '/help':
        return usage()

    if cmd_str == '/list':
        return show_list(args[0])

    if cmd_str == '/teach':
        return teach(args[0])

    if cmd_str == '/wiki':
        return wiki(args[0])

    if cmd_str == '/cat':
        return cat(args[0])

    if cmd_str == '/py':
        return py_eval(args[0])

    if cmd_str == '/fortune':
        return fortune()


def handle(cmd_str, subdomain, channel, user):
    cmds = map(lambda x: encode_from_unicode(x), clever_split(cmd_str))
    subdomain = encode_from_unicode(subdomain)
    channel = encode_from_unicode(channel)
    user = encode_from_unicode(user)

    # 后面的链接中要求字符串为 ascii 串而不能是 unicode 串
    user_link = 'https://%s.bearychat.com/messages/@%s' % (subdomain, user)
    user_ref = '[@%s](%s)' % (user, user_link)
    result = {}

    if len(cmds) > 0:
        bot_response = call_command(cmds[0], cmds[1:])
        if isinstance(bot_response, str) or isinstance(bot_response, unicode):
            result.setdefault('text', user_ref + '\n' + bot_response)
        elif isinstance(bot_response, dict):
            result.setdefault('text', user_ref)
            result.update(bot_response)
        else:
            result.setdefault('text', 'Your command is error.')

    else:
        bot_response = call_command('/fortune')
        result.setdefault('text', user_ref + '\n' + bot_response)

    return result
